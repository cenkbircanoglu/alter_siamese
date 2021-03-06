# coding=utf-8
from __future__ import absolute_import

import torch
from torch import nn
from torch.autograd import Variable


class ATriplet(nn.Module):
    def __init__(self, alpha=40, beta=4):
        super(ATriplet, self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.use_cuda = False

    def forward(self, inputs, targets):
        n = inputs.size(0)
        # Compute pairwise distance
        dist_mat = euclidean_dist(inputs)
        eyes_ = Variable(torch.eye(n, n))
        if self.use_cuda:
            targets = targets.cuda()
            eyes_ = eyes_.cuda()

        pos_mask = targets.expand(n, n).eq(targets.expand(n, n).t())
        neg_mask = eyes_.eq(eyes_) - pos_mask
        pos_mask = pos_mask - eyes_.eq(1)

        pos_dist = torch.masked_select(dist_mat, pos_mask)
        neg_dist = torch.masked_select(dist_mat, neg_mask)

        num_instances = len(pos_dist) // n + 1
        num_neg_instances = n - num_instances

        pos_dist = pos_dist.resize(len(pos_dist) // (num_instances - 1), num_instances - 1)
        neg_dist = neg_dist.resize(len(neg_dist) // num_neg_instances, num_neg_instances)

        loss = list()
        num_valid_triplets = 0

        for i, pos_pair in enumerate(pos_dist):
            pos_pair = pos_dist[i]
            neg_pair = neg_dist[i]

            pos_logit = torch.sum(torch.exp(self.alpha * (1 - pos_pair)))
            neg_logit = torch.sum(torch.exp(self.alpha * (1 - neg_pair)))
            a_lr = 1 - (pos_logit / (pos_logit + neg_logit)).data[0]

            if i % 37 == 0:
                print(3 * '#', '%.2f' % a_lr)

            pos_pair = pos_pair.repeat(num_neg_instances, 1)
            neg_pair = neg_pair.repeat((num_instances - 1), 1).t()

            triplet_mat = torch.log(torch.exp(self.beta * (pos_pair - neg_pair)) + 1)
            triplet_mask = triplet_mat > 0.65
            valid_triplets = torch.masked_select(triplet_mat, triplet_mask)

            num_valid_triplets += torch.sum(triplet_mask).data[0]
            loss_ = a_lr * torch.mean(valid_triplets)
            loss.append(loss_)

        return 0 * torch.sum(pos_pair) if num_valid_triplets == 0 else (1 / num_valid_triplets) * torch.sum(
            torch.cat(loss))

    def cuda(self, device_id=None):
        """Moves all model parameters and buffers to the GPU.

        Arguments:
            device_id (int, optional): if specified, all parameters will be
                copied to that device
        """
        self.use_cuda = True
        return self._apply(lambda t: t.cuda(device_id))


def euclidean_dist(inputs_):
    n = inputs_.size(0)
    dist = torch.pow(inputs_, 2).sum(dim=1, keepdim=True).expand(n, n)
    dist = dist + dist.t()
    dist.addmm_(1, -2, inputs_, inputs_.t())
    # for numerical stability
    dist = dist.clamp(min=1e-12).sqrt()
    return dist


def main():
    data_size = 32
    input_dim = 3
    output_dim = 2
    num_class = 16
    # margin = 0.5
    x = Variable(torch.rand(data_size, input_dim), requires_grad=False)
    w = Variable(torch.rand(input_dim, output_dim), requires_grad=True)
    inputs = x.mm(w)
    y_ = 8 * list(range(num_class))
    targets = Variable(torch.IntTensor(y_))

    print(ATriplet(alpha=4)(inputs, targets))


if __name__ == '__main__':
    main()
    print('Congratulations to you!')
