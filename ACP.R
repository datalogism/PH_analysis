#Plusieurs packages pour faire de l'ADD sous R
#Choix d'utiliser deux packages : FactoMineR (pour l'analyse) et factoextra (pour la visualisation, des donn???es, bas???e sur ggplot2)
install.packages(c("FactoMineR", "factoextra"))
library("FactoMineR")
library("factoextra")

#
# Importation des donn???es -----------------------
#
d<-read.csv2("C:/Users/Celian/Desktop/PH_study/list_cleaned_2.csv",header=TRUE,sep=";",dec=",",encoding = "UTF-8") #lecture d'un fichier csv
d_num<-data.matrix(d[,c(4:12,15)])
d_norm<-sweep(d_num, 2, colSums(d_num), FUN = "/")
#==================== Graphique correlation
cormat <- round(cor(d_norm),2)
# Heatmap
library(ggplot2)
# Obtenir le triangle supérieur
get_upper_tri <- function(cormat){
  cormat[lower.tri(cormat)]<- NA
  return(cormat)
}
upper_tri <- get_upper_tri(cormat)

library(reshape2)
melted_cormat <- melt(upper_tri, na.rm = TRUE)

ggplot(data = melted_cormat, aes(Var2, Var1, fill = value))+
  geom_tile(color = "white")+
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                       midpoint = 0, limit = c(-1,1), space = "Lab",
                       name="Pearson\nCorrelation") +
  theme_minimal()+ 
  theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                   size = 12, hjust = 1))+
  coord_fixed()
d<-read.csv2("C:/Users/Celian/Desktop/PH_study/list_cleaned_orcid.csv",header=TRUE,sep=";",dec=",",encoding = "UTF-8") #lecture d'un fichier csv
d_focus<-d[,c(13,16:28)]
d_focus$fr_contrib<-as.factor(d_focus$fr_contrib)
d_focus$en_contrib<-as.factor(d_focus$en_contrib)
d_focus$pt_contrib<-as.factor(d_focus$pt_contrib)
d_focus$es_contrib<-as.factor(d_focus$es_contrib)
d_focus$authors_contrib<-as.factor(d_focus$authors_contrib)
d_focus$reviewers_contrib<-as.factor(d_focus$reviewers_contrib)
d_focus$translator_contrib<-as.factor(d_focus$translator_contrib)
d_focus$editor_contrib<-as.factor(d_focus$editor_contrib)
res.mca = MCA(d_focus, quanti.sup=c(1), quali.sup=c(12:14))


plot.MCA(res.mca, invisible=c("var","quali.sup"), cex=0.7)
plot.MCA(res.mca, invisible=c("ind","quali.sup"), cex=0.7)
plot.MCA(res.mca, invisible=c("ind"))
plot.MCA(res.mca, invisible=c("ind", "var"))