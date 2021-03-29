# -*- coding:utf-8 -*-
"""
@author:Zehui Yu
@file: validation_rod2021.py
@time: 2021/01/31
"""
import sys
import os

from cruw import CRUW
from cruw.eval import evaluate_rod2021, evaluate_rod2021_APAR
import argparse
from rodnet.utils.load_configs import load_configs_from_file


"python tools/validation_rod2021.py --config configs/my_config_rodnet_hg1_win16_lovasz_bs16_lr1e5_2020_2_11.py " \
" --checkpoint_name rodnet-hg1-win16-wobg-lovasz_bs16_lr1e5_2020_2_11-20210211-103511"
def parse_args():
    parser = argparse.ArgumentParser(description='Test RODNet.')
    parser.add_argument('--config', type=str, help='choose rodnet model configurations')
    parser.add_argument('--checkpoint_name', type=str, default='./data/', help='directory to the prepared data')
    args = parser.parse_args()
    return args


def eval_rod2021_batch(config_file, checkpoint_name):
    config_dict = load_configs_from_file(args.config)
    epoch_start, epoch_end = 1, config_dict['train_cfg']['n_epoch']
    pkl_idx = list(range(epoch_start, epoch_end + 1))
    for i in pkl_idx:
        data_root = config_dict['dataset_cfg']['pkl_root']
        cmd = 'python /nfs/volume-95-8/tianwanxin/RODNet/tools/validation.py --config /nfs/volume-95-8/tianwanxin/RODNet/%s \
        --data_dir %s  \
        --valid \
        --checkpoint /nfs/volume-95-8/tianwanxin/RODNet/checkpoints/%s/epoch_%02d_final.pkl' % (config_file, data_root, checkpoint_name, i)
        os.system(cmd)

        valid_res_dir = '/nfs/volume-95-8/tianwanxin/RODNet/valid_res/'
        res_dir = os.path.join(valid_res_dir, checkpoint_name)
        dataset = CRUW(data_root="/nfs/volume-95-8/ROD_Challenge/src_dataset", sensor_config_name='sensor_config_rod2021')
        submit_dir = '/nfs/volume-95-8/tianwanxin/RODNet/valid_results/%s' % checkpoint_name
        # truth_dir = '/nfs/volume-95-8/aocheng/RODNeto/data/scene_ave/for_valid'
        truth_dir = config_dict['dataset_cfg']['val_root']
        AP, AR = evaluate_rod2021_APAR(submit_dir, truth_dir, dataset)
        # print('epoch: %d, AP: %.4f, AR: %.4f' % (i, AP, AR))
        if not os.path.exists(res_dir):
            os.makedirs(res_dir)
        with open('/nfs/volume-95-8/tianwanxin/RODNet/valid_res/%s/valid_res.txt' % checkpoint_name, 'a') as f:
            f.write('epoch: %d, AP: %.4f, AR: %.4f\n' % (i, AP, AR))


if __name__ == '__main__':
    # data_root = "/nfs/volume-95-8/ROD_Challenge/src_dataset"
    # dataset = CRUW(data_root=data_root, sensor_config_name='sensor_config_rod2021')
    # submit_dir = '/nfs/volume-95-8/ROD_Challenge/RODNet/tools/valid_results/rodnet-hg1-win16-wobg-20210206-124028'
    # truth_dir = '/nfs/volume-95-8/ROD_Challenge/RODNet/for_validation/gt_zixiang_split'
    # ap, ar = evaluate_rod2021_APAR(submit_dir, truth_dir, dataset)
    # print(ap, ar)
    args = parse_args()
    eval_rod2021_batch(args.config, args.checkpoint_name)
