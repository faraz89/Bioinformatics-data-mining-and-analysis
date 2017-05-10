## Faraz Khan 04.07.16
rm(list=ls())
library(edgeR)
options(scipen = 500) # bias against scientific notation
options(digits = 1) # show fewer decimal places

samples <- read.csv("bamGnut_adac1040_counts_data_no-absent_simple.csv",row.names=1)
x = samples[,c(4,8,12,14,16,18)]
group <- factor(c(1,1,1,2,2,2)) #group samples.
y <- DGEList(counts=x,group=group) #create DGElist
dim(y)
## Since the smallest group size is Three, we keep genes that achieve at least one count per million (cpm) in at least Three samples:
keep <- rowSums(cpm(y)>1) >= 3
y <- y[keep, , keep.lib.sizes=FALSE]
#dim(y)
## Re-compute the library sizes:
y$samples$lib.size <- colSums(y$counts)
## Compute effective library sizes using TMM normalization:
y <- calcNormFactors(y)
edgeR.cpm.norm1 = cpm(y, normalized.sizes = TRUE)
# Save the cpm values
library(data.table) 
edgeR.cpm.norm1 <- as.data.frame(edgeR.cpm.norm1)
edgeR.cpm.norm1 = setDT(edgeR.cpm.norm1, keep.rownames = T)[]
edgeR.cpm.norm1 = as.data.frame (edgeR.cpm.norm1)
write.csv (edgeR.cpm.norm1, "cpm.norm.csv", sep = "\t")
y$samples
#create MDS plot shows variation between samples
colors <- rep(c("red", "blue"), 3)
plotMDS(y, col=colors[group], pch=.2)
pdf("allDipCsamples.pdf")
plotMDS(y)
dev.off()
getPriorN(y)
y <- estimateCommonDisp(y)
y <- estimateTagwiseDisp(y, prior.df = 20)
y$common.dispersion
plotBCV(y)
et <- exactTest(y)
top <- topTags(et)
top
## Check the individual cpm values for the top genes:
cpm(y)[rownames(top), ]
## The total number of DE genes at 5% FDR is given by:
summary(de <- decideTestsDGE(et, p=0.05, adjust="BH"))
## Plot the log-fold-changes, highlighting the DE genes:
detags <- rownames(y)[as.logical(de)]
plotSmear(et, de.tags=detags)
abline(h=c(-1, 1), col="blue")
##(The blue lines indicate 2-(log)-fold changes
allResults <- topTags( et , n = nrow( et$table ) )$table
write.table(detags, file="19vs31.csv",row.names=FALSE,col.names=FALSE,quote=FALSE)
#MAplot
head(allResults)
with(allResults, plot(logCPM, logFC, pch=20, cex=.8,  main="logFC vs Abundance")
with(subset(allResults, FDR<0.05), points(logCPM, logFC, cex=.8 ,pch=20, col="red"))
abline(h = c(-1, 0, 1), col = c("dodgerblue", "yellow", "dodgerblue"), lty=2)


