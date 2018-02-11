import os

PAR = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), '../'))


class BaseConfig(object):
    def __init__(self, data_name=None, batch_size=32, epochs=20, num_workers=1, channel=1, cuda=False, loss=None,
                 embedding=128, loader_name=None, network=None, **kwargs):
        self.data_dir = os.path.join(PAR, 'data')
        self.result_dir = os.path.join(PAR, './results/%s/%s/%s' % (data_name, network, loss))
        self.log_path = os.path.join(PAR, './results/%s/%s/%s.log' % (data_name, network, loss))
        self.tr_dir = os.path.join(self.data_dir, '%s/train/' % data_name)
        self.te_dir = os.path.join(self.data_dir, '%s/test/' % data_name)
        self.batch_size = 64
        self.epochs = epochs
        self.num_workers = num_workers
        self.channel = channel
        self.cuda = True
        self.loss = loss
        self.embedding = embedding
        self.trainer = None
        self.loader_name = loader_name

    @property
    def network_channel(self):
        return self.channel
