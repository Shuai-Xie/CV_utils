from torchviz import make_dot
from torchsummary import summary
import torch
from torchvision.models.resnet import resnet18  # demo
from torchvision.models.mobilenet import mobilenet_v2


# visualize model architure

def model_vis(model, input):
    g = make_dot(model(input), params=dict(model.named_parameters()))  # can't vis model which returns a list
    g.view()


def model_summary(net, input_size):
    """
    :param net:
    :param input_size: C,H,W
    :return:
    """
    summary(net, input_size, device='cpu')


# see model layers

def model_layers(model):
    # model.named_parameters() 与 model.state_dict() 相比，少了 运行过程中 bn
    print('{:>4} {:<50} {:<30} {}'.format('idx', 'param', 'size', 'grad'))
    for idx, (name, param) in enumerate(model.named_parameters()):  # recurse=True, as net itself is a big module
        print('{:>4} {:<50} {:<30} {}'.format(idx, name, str(param.size()), param.requires_grad))


def model_params(net):
    print('=> model params:')
    params = list(net.parameters())
    k = 0
    for idx, layer in enumerate(params):
        # print(type(layer))  # torch.nn.parameter.Parameter, Parameter(torch.Tensor)
        # layer is actually a tensor
        print('layer (%d):' % idx, layer.size(), end=', ')
        mul = 1
        for v in layer.size():  # [out_C, in_C, kernel_w, kernel_h]
            mul *= v
        print('params:', mul)
        k += mul
    print('total params:', k)


if __name__ == '__main__':
    m1 = resnet18(pretrained=False)
    m2 = mobilenet_v2(pretrained=False)  # If True, returns a model pre-trained on ImageNet

    # model_params(m1)
    model_params(m2)


# load/save model

def load_model(model, model_path,
               optimizer=None, resume=False,
               lr=None, lr_step=None):
    """
    load a model from pretrain, same layer use pretrain, different layer use default
    """
    # 1.load ckpt
    checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)
    print('loaded {}, epoch {}'.format(model_path, checkpoint['epoch']))  # resdcn18, epoch=140, 1x; 2x, epoch=230

    # 2.judge model and ckpt state_dict, so that ckpt can be loaded

    # from checkpoint
    state_dict_ = checkpoint['state_dict']  # just an OrderedDict
    state_dict = {}
    # convert data_parallal to model! a way to deal with data_parallal weights
    for k in state_dict_:
        if k.startswith('module') and not k.startswith('module_list'):
            state_dict[k[7:]] = state_dict_[k]  # k[7:] remove module.
        else:
            state_dict[k] = state_dict_[k]

    # from defined model
    model_state_dict = model.state_dict()

    msg = 'msg'

    # check loaded parameters and created model parameters
    # judge whether: model_state_dict = ckpt state_dict
    for k in state_dict:
        if k in model_state_dict:
            # if ckpt has this k, but shape different, maybe different num_classes
            if state_dict[k].shape != model_state_dict[k].shape:  # may be shape diff
                print('Skip loading parameter {}, required shape {}, loaded shape {}. {}'.
                      format(k, model_state_dict[k].shape, state_dict[k].shape, msg))
                state_dict[k] = model_state_dict[k]
        else:
            # different task, miss heads keys
            print('Drop parameter {}.'.format(k) + msg)

    for k in model_state_dict:
        if k not in state_dict:  # reverse of last else, complement state_dict so that it can be load!
            print('No param {}.'.format(k) + msg)
            state_dict[k] = model_state_dict[k]

    # model_layers(model)

    # load ckpt done!
    model.load_state_dict(state_dict, strict=False)

    # 3.resume optimizer parameters
    if optimizer is not None and resume:
        if 'optimizer' in checkpoint:  # if ckpt has saved optimizer
            optimizer.load_state_dict(checkpoint['optimizer'])
            start_epoch = checkpoint['epoch']  # resume epoch
            start_lr = lr
            for step in lr_step:  # traverse each lr_step, get the last start_lr
                if start_epoch >= step:
                    start_lr *= 0.1
            for param_group in optimizer.param_groups:
                param_group['lr'] = start_lr  # set new lr for optimizer
            print('Resumed optimizer with start lr', start_lr)
        else:
            print('No optimizer parameters in checkpoint.')

    if optimizer is not None:
        start_epoch = 0
        return model, optimizer, start_epoch
    else:
        return model


def save_model(path, epoch, model, optimizer=None):
    """
    save model and optimizer
    """
    if isinstance(model, torch.nn.DataParallel):
        state_dict = model.module.state_dict()  # convert data_parallal to model
    else:
        state_dict = model.state_dict()
    data = {
        'epoch': epoch,
        'state_dict': state_dict
    }
    if optimizer is not None:
        data['optimizer'] = optimizer.state_dict()
    torch.save(data, path)
