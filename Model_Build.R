setwd("~/Documents/!Research/Github/NBA")

library(e1071)

#Load Training Data
train<-read.csv("data515.csv")
train_515r=train[,c("Def.FTFGA_a_5", "EFG_a_5", "EFG_h_15", "Win.Pct_a_15", "Win.Pct_h_15", "Def.EFG_h_15", "Def.TOV_h_15", "FTFGA_h_15", "TOV_h_15", "Win_5")]
train_515r=cbind(train_515r[,-ncol(train_515r)], yvar=as.factor(train_515r[,"Win_5"]))
p2.model<-svm(yvar~., data=train_515r, kernel="linear", cost=.01, type="C")     #have to update cost/gamma/degree.  linear, radial, polynomial, possibly train.p2a

#Load Testing Data
#test_full<-read.csv('data515test.csv')
test_full<-read.csv('data515.csv')
test=test_full[,c("Def.FTFGA_a_5", "EFG_a_5", "EFG_h_15", "Win.Pct_a_15", "Win.Pct_h_15", "Def.EFG_h_15", "Def.TOV_h_15", "FTFGA_h_15", "TOV_h_15", "Win_5")]
predvect<-predict(p2.model, newdata=test) 
predvect[predvect> .4] <- 1    
predvect[predvect<=.4] <-0
predvect<-cbind(predvect, test_full[,c("Win_5", "Game_ID")])
table(predvect[,"predvect"], predvect[,"Win_5"])

#find CV accuracy with just training data
fit_svm.l(train_515r, c(.001, .01, .1, 1, 5, 25))

#necessary functions to cross validate and provide accuracy
fit_svm.l<-function(train, cost_vect) {
  library(e1071)
  tune.linear<-tune(svm, yvar~., data=train, kernel="linear", ranges=list(cost=cost_vect), type="C")   
  param<-tune.linear$best.parameters
  acc<-1-tune.linear$best.performance
  return (data.frame(acc, method=paste0("svc, cost:", param[1])))
}