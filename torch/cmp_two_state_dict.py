model_state_dict = [
    'conv1.weight', 'bn1.weight', 'bn1.bias', 'bn1.running_mean', 'bn1.running_var', 'bn1.num_batches_tracked', 'layer1.0.conv1.weight',
    'layer1.0.bn1.weight', 'layer1.0.bn1.bias', 'layer1.0.bn1.running_mean', 'layer1.0.bn1.running_var', 'layer1.0.bn1.num_batches_tracked',
    'layer1.0.conv2.weight', 'layer1.0.bn2.weight', 'layer1.0.bn2.bias', 'layer1.0.bn2.running_mean', 'layer1.0.bn2.running_var',
    'layer1.0.bn2.num_batches_tracked', 'layer1.1.conv1.weight', 'layer1.1.bn1.weight', 'layer1.1.bn1.bias', 'layer1.1.bn1.running_mean',
    'layer1.1.bn1.running_var', 'layer1.1.bn1.num_batches_tracked', 'layer1.1.conv2.weight', 'layer1.1.bn2.weight', 'layer1.1.bn2.bias',
    'layer1.1.bn2.running_mean', 'layer1.1.bn2.running_var', 'layer1.1.bn2.num_batches_tracked', 'layer2.0.conv1.weight', 'layer2.0.bn1.weight',
    'layer2.0.bn1.bias', 'layer2.0.bn1.running_mean', 'layer2.0.bn1.running_var', 'layer2.0.bn1.num_batches_tracked', 'layer2.0.conv2.weight',
    'layer2.0.bn2.weight', 'layer2.0.bn2.bias', 'layer2.0.bn2.running_mean', 'layer2.0.bn2.running_var', 'layer2.0.bn2.num_batches_tracked',
    'layer2.0.downsample.0.weight', 'layer2.0.downsample.1.weight', 'layer2.0.downsample.1.bias', 'layer2.0.downsample.1.running_mean',
    'layer2.0.downsample.1.running_var', 'layer2.0.downsample.1.num_batches_tracked', 'layer2.1.conv1.weight', 'layer2.1.bn1.weight',
    'layer2.1.bn1.bias', 'layer2.1.bn1.running_mean', 'layer2.1.bn1.running_var', 'layer2.1.bn1.num_batches_tracked', 'layer2.1.conv2.weight',
    'layer2.1.bn2.weight', 'layer2.1.bn2.bias', 'layer2.1.bn2.running_mean', 'layer2.1.bn2.running_var', 'layer2.1.bn2.num_batches_tracked',
    'layer3.0.conv1.weight', 'layer3.0.bn1.weight', 'layer3.0.bn1.bias', 'layer3.0.bn1.running_mean', 'layer3.0.bn1.running_var',
    'layer3.0.bn1.num_batches_tracked', 'layer3.0.conv2.weight', 'layer3.0.bn2.weight', 'layer3.0.bn2.bias', 'layer3.0.bn2.running_mean',
    'layer3.0.bn2.running_var', 'layer3.0.bn2.num_batches_tracked', 'layer3.0.downsample.0.weight', 'layer3.0.downsample.1.weight',
    'layer3.0.downsample.1.bias', 'layer3.0.downsample.1.running_mean', 'layer3.0.downsample.1.running_var',
    'layer3.0.downsample.1.num_batches_tracked', 'layer3.1.conv1.weight', 'layer3.1.bn1.weight', 'layer3.1.bn1.bias',
    'layer3.1.bn1.running_mean', 'layer3.1.bn1.running_var', 'layer3.1.bn1.num_batches_tracked', 'layer3.1.conv2.weight', 'layer3.1.bn2.weight',
    'layer3.1.bn2.bias', 'layer3.1.bn2.running_mean', 'layer3.1.bn2.running_var', 'layer3.1.bn2.num_batches_tracked', 'layer4.0.conv1.weight',
    'layer4.0.bn1.weight', 'layer4.0.bn1.bias', 'layer4.0.bn1.running_mean', 'layer4.0.bn1.running_var', 'layer4.0.bn1.num_batches_tracked',
    'layer4.0.conv2.weight', 'layer4.0.bn2.weight', 'layer4.0.bn2.bias', 'layer4.0.bn2.running_mean', 'layer4.0.bn2.running_var',
    'layer4.0.bn2.num_batches_tracked', 'layer4.0.downsample.0.weight', 'layer4.0.downsample.1.weight', 'layer4.0.downsample.1.bias',
    'layer4.0.downsample.1.running_mean', 'layer4.0.downsample.1.running_var', 'layer4.0.downsample.1.num_batches_tracked',
    'layer4.1.conv1.weight', 'layer4.1.bn1.weight', 'layer4.1.bn1.bias', 'layer4.1.bn1.running_mean', 'layer4.1.bn1.running_var',
    'layer4.1.bn1.num_batches_tracked', 'layer4.1.conv2.weight', 'layer4.1.bn2.weight', 'layer4.1.bn2.bias', 'layer4.1.bn2.running_mean',
    'layer4.1.bn2.running_var', 'layer4.1.bn2.num_batches_tracked', 'deconv_layers.0.weight', 'deconv_layers.0.bias',
    'deconv_layers.0.conv_offset_mask.weight', 'deconv_layers.0.conv_offset_mask.bias', 'deconv_layers.1.weight', 'deconv_layers.1.bias',
    'deconv_layers.1.running_mean', 'deconv_layers.1.running_var', 'deconv_layers.1.num_batches_tracked', 'deconv_layers.3.weight',
    'deconv_layers.4.weight', 'deconv_layers.4.bias', 'deconv_layers.4.running_mean', 'deconv_layers.4.running_var',
    'deconv_layers.4.num_batches_tracked', 'deconv_layers.6.weight', 'deconv_layers.6.bias', 'deconv_layers.6.conv_offset_mask.weight',
    'deconv_layers.6.conv_offset_mask.bias', 'deconv_layers.7.weight', 'deconv_layers.7.bias', 'deconv_layers.7.running_mean',
    'deconv_layers.7.running_var', 'deconv_layers.7.num_batches_tracked', 'deconv_layers.9.weight', 'deconv_layers.10.weight',
    'deconv_layers.10.bias', 'deconv_layers.10.running_mean', 'deconv_layers.10.running_var', 'deconv_layers.10.num_batches_tracked',
    'deconv_layers.12.weight', 'deconv_layers.12.bias', 'deconv_layers.12.conv_offset_mask.weight', 'deconv_layers.12.conv_offset_mask.bias',
    'deconv_layers.13.weight', 'deconv_layers.13.bias', 'deconv_layers.13.running_mean', 'deconv_layers.13.running_var',
    'deconv_layers.13.num_batches_tracked', 'deconv_layers.15.weight', 'deconv_layers.16.weight', 'deconv_layers.16.bias',
    'deconv_layers.16.running_mean', 'deconv_layers.16.running_var', 'deconv_layers.16.num_batches_tracked', 'hm.0.weight', 'hm.0.bias',
    'hm.2.weight', 'hm.2.bias', 'wh.0.weight', 'wh.0.bias', 'wh.2.weight', 'wh.2.bias', 'reg.0.weight', 'reg.0.bias', 'reg.2.weight',
    'reg.2.bias']

model_named_params = [
    'conv1.weight', 'bn1.weight', 'bn1.bias', 'layer1.0.conv1.weight', 'layer1.0.bn1.weight', 'layer1.0.bn1.bias', 'layer1.0.conv2.weight',
    'layer1.0.bn2.weight', 'layer1.0.bn2.bias', 'layer1.1.conv1.weight', 'layer1.1.bn1.weight', 'layer1.1.bn1.bias', 'layer1.1.conv2.weight',
    'layer1.1.bn2.weight', 'layer1.1.bn2.bias', 'layer2.0.conv1.weight', 'layer2.0.bn1.weight', 'layer2.0.bn1.bias', 'layer2.0.conv2.weight',
    'layer2.0.bn2.weight', 'layer2.0.bn2.bias', 'layer2.0.downsample.0.weight', 'layer2.0.downsample.1.weight', 'layer2.0.downsample.1.bias',
    'layer2.1.conv1.weight', 'layer2.1.bn1.weight', 'layer2.1.bn1.bias', 'layer2.1.conv2.weight', 'layer2.1.bn2.weight', 'layer2.1.bn2.bias',
    'layer3.0.conv1.weight', 'layer3.0.bn1.weight', 'layer3.0.bn1.bias', 'layer3.0.conv2.weight', 'layer3.0.bn2.weight', 'layer3.0.bn2.bias',
    'layer3.0.downsample.0.weight', 'layer3.0.downsample.1.weight', 'layer3.0.downsample.1.bias', 'layer3.1.conv1.weight',
    'layer3.1.bn1.weight', 'layer3.1.bn1.bias', 'layer3.1.conv2.weight', 'layer3.1.bn2.weight', 'layer3.1.bn2.bias', 'layer4.0.conv1.weight',
    'layer4.0.bn1.weight', 'layer4.0.bn1.bias', 'layer4.0.conv2.weight', 'layer4.0.bn2.weight', 'layer4.0.bn2.bias',
    'layer4.0.downsample.0.weight', 'layer4.0.downsample.1.weight', 'layer4.0.downsample.1.bias', 'layer4.1.conv1.weight',
    'layer4.1.bn1.weight', 'layer4.1.bn1.bias', 'layer4.1.conv2.weight', 'layer4.1.bn2.weight', 'layer4.1.bn2.bias', 'deconv_layers.0.weight',
    'deconv_layers.0.bias', 'deconv_layers.0.conv_offset_mask.weight', 'deconv_layers.0.conv_offset_mask.bias', 'deconv_layers.1.weight',
    'deconv_layers.1.bias', 'deconv_layers.3.weight', 'deconv_layers.4.weight', 'deconv_layers.4.bias', 'deconv_layers.6.weight',
    'deconv_layers.6.bias', 'deconv_layers.6.conv_offset_mask.weight', 'deconv_layers.6.conv_offset_mask.bias', 'deconv_layers.7.weight',
    'deconv_layers.7.bias', 'deconv_layers.9.weight', 'deconv_layers.10.weight', 'deconv_layers.10.bias', 'deconv_layers.12.weight',
    'deconv_layers.12.bias', 'deconv_layers.12.conv_offset_mask.weight', 'deconv_layers.12.conv_offset_mask.bias', 'deconv_layers.13.weight',
    'deconv_layers.13.bias', 'deconv_layers.15.weight', 'deconv_layers.16.weight', 'deconv_layers.16.bias', 'hm.0.weight', 'hm.0.bias',
    'hm.2.weight', 'hm.2.bias', 'wh.0.weight', 'wh.0.bias', 'wh.2.weight', 'wh.2.bias', 'reg.0.weight', 'reg.0.bias', 'reg.2.weight',
    'reg.2.bias']


def cmp_state_list(l1, l2):
    diff_param = set(l1).symmetric_difference(set(l2))
    l = l1 if len(l1) > len(l2) else l2
    diff = []
    for p in diff_param:
        diff.append((l.index(p), p))
    diff = sorted(diff, key=lambda t: t[0])  # sort by layer idx
    for idx, d in enumerate(diff):
        print('{}: {}'.format(idx, d))
    print('l1: {}, l2: {}, diff: {}'.format(len(l1), len(l2), len(diff)))


cmp_state_list(model_named_params, model_state_dict)
