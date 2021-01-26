gen=list()
for(x in seq(12)){
   infile<-sprintf("./plainfile/gt_chr%02d.txt",x)
   gen[[x]]<-as.matrix(read.table(infile,header=F)[,-(1:2)] )
}

map=list()
for(x in seq(12)){
   infile<-sprintf("./plainfile/map_chr%02d.txt",x)
   map[[x]]<-read.table(infile,header=T)
}

Rice=list()
Rice[["gen"]]<-gen
Rice[["map"]]<-map
save(Rice,file='Rice.RData')



