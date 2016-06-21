setwd("~/Documents/!Research/Github/NBA")

#Import Libraries
library(e1071)
library(tree)
library(randomForest)
library(neuralnet)
library(gbm)

#Load Training Data
train<-read.csv("data515.csv")
train515=train[,-which(names(train)%in% c('Game_ID', 'Home_5', 'Win_5', 'n.games_a_5', 'n.games_h_5', 'Home_15', 'Win_15'))]
train515=cbind(train515, yvar=train$Win_5)


#Variable Selection
#Tree Methods
train515$yvar<-factor(train515$yvar)    
tree.model<-tree(yvar~., train515)      
summary(tree.model)
plot(tree.model)
text(tree.model, cex=0.5)

prune5 <- prune.misclass(tree.model,best=8)  
summary(prune5)
plot(prune5)
text(prune5, cex=1)

ran.model <- randomForest(yvar~., data=train515, mtry=5) 
summary(ran.model)

#doesn't work
nn<-neuralnet(yvar~ORB_a_5+ORB_h_5, data=train515, hidden=c(3,3), rep=5)
plot(nn)
pred<-compute(nn, iris[-5])$net.result

#gradient boosting
gb=gbm(yvar~., data=train515, cv.folds=5)
gb$cv.error

#next to do: .  look up neural networks.  look up gradient boosting

### Neural Network
fit_nn<-function(train) {
  library(neuralnet)
  nn<-neuralnet(yvar~m1, data=train, hidden=c(3,3), rep=5)
  plot(nn)
  pred<-compute(nn, iris[-5])$net.result
}


Generalized Boosting Model
#i tried using this, but it crashed my computer, lol


#old stuff

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