#!/usr/bin/env bash


# 24998
EPOCHS=500
for network in net_64 alex_64 dense_64
do
    for data in cats_dogs
    do
        # Listwise
        for loss in CrossEntropyLoss MultiMarginLoss  FocalLoss SoftmaxLoss CenterLoss  MultiClassHingeLoss  HistogramLoss
        do
              python __main__.py listwise --data_name $data --width 64 --height 64 --channel 3 \
                --network $network --embedding 2 --epochs $EPOCHS --loss $loss --loader_name data_loaders
        done
    done
done

#for network in angle_net_64 angle_alex_64 #angle_dense_64
#do
#    for data in cats_dogs
#    do
#        # Listwise
#        for loss in AngleLoss
#        do
#              python __main__.py listwise --data_name $data --width 64 --height 64 --channel 3 \
#                --network $network --embedding 2 --epochs $EPOCHS --loss $loss --loader_name data_loaders
#        done
#    done
#done