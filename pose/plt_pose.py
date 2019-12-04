import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cmx
import numpy as np
import cv2
import math
from box.box_utils import pt_in_img

np.set_printoptions(suppress=True)

num_class = 20

mpl.rcParams['legend.fontsize'] = 6
# use cmap color | tab20, tab20b, hsv
cmap = plt.get_cmap('tab20')  # qualitative cmaps, >18
cNorm = mcolors.Normalize(vmin=0, vmax=num_class - 1)
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cmap)


def plt_2d_skeleton_MP(image, pose2Ds, joints_link,
                       imgname=None, show_person_id=False,
                       plt_show=True, out_path=None):
    img_h, img_w, _ = image.shape
    # plt.figure(figsize=(img_w / 100.0, img_h / 100.0))
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    plt.imshow(image)

    if pose2Ds.shape[0] > 0:
        # (N,16,2) -> (N,2,16)
        pose2Ds = np.transpose(pose2Ds, (0, 2, 1))

        # plt each person pose
        for person_idx, pose2D in enumerate(pose2Ds):
            # plt bones
            for idx, link in enumerate(joints_link):
                pt_A, pt_B = pose2D[:, link[0]], pose2D[:, link[1]]
                # A,B valid, then plt bone
                if pt_in_img(pt_A) and pt_in_img(pt_B):
                    plt.plot(pose2D[0, link], pose2D[1, link],
                             color=scalarMap.to_rgba(idx),
                             linewidth=3.0)
            if show_person_id:
                head = pose2D[:, 0]
                plt.text(head[0], head[1] + 30, s=str(person_idx + 1))
    else:
        print('no persons!')

    if imgname:
        plt.title(imgname, fontsize=12)

    if out_path:
        plt.savefig(out_path,
                    # bbox_inches="tight", # make sure plot has same size
                    # pad_inches=0.0
                    )
    if plt_show:
        plt.show()
    else:
        plt.close('all')


def plt_3d_skeleton_MP(pose3Ds, joints_link, imgname=None,
                       azims=(-90, -45, 0, 45, 90),
                       plt_show=True, out_path=None):
    fig = plt.figure(figsize=(len(azims) * 6, 6))
    # if imgname:
    #     fig.suptitle(imgname, fontsize=14, fontweight='bold')
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    # already transpose
    pose3Ds = np.transpose(pose3Ds, (0, 2, 1))  # (N,3,18)

    for i in range(len(azims)):
        ax = fig.add_subplot(1, len(azims), i + 1, projection='3d')
        ax.axis('off')  # close axis

        # plt each person pose
        for person_idx, pose3D in enumerate(pose3Ds):
            # plt bones
            for idx, link in enumerate(joints_link):  # [0,1,2] -> [x,y,z]
                pt_A, pt_B = pose3D[:, link[0]], pose3D[:, link[1]]
                # A,B valid, then plt bone
                if pt_A[0] >= 0 and pt_A[1] >= 0 and pt_B[0] >= 0 and pt_B[1] >= 0:
                    ax.plot(pose3D[0, link], pose3D[2, link], -pose3D[1, link],  # [X],[Y],[Z] 画线
                            # color=scalarMap.to_rgba(idx),
                            linewidth=5.0)

            head = pose3D[:, 0]
            ax.text(head[0], 0, -head[1] + 30, s=str(person_idx + 1))  # has z coord

        ax.view_init(azim=azims[i], elev=15)  # 15° 看到的人更正

        ax.set_xlabel('X')
        ax.set_ylabel('Z')  # exchange Z,Y, for visualizing better
        ax.set_zlabel('Y')
        ax.set_aspect('equal')

        # all person's x,y,z
        X = pose3Ds[:, 0, :]
        X[np.where(X < 0)] = X.max()  # remove x=-1
        Y = pose3Ds[:, 2, :]
        Z = -pose3Ds[:, 1, :]  # real Y
        Z[np.where(Z > 0)] = Z.min()  # remove y=-1

        max_range = np.array([X.max() - X.min(), Y.max() - Y.min(), Z.max() - Z.min()]).max() / 2.0

        mid_x = (X.max() + X.min()) * 0.5  # 219
        mid_y = (Y.max() + Y.min()) * 0.5  # 215
        mid_z = (Z.max() + Z.min()) * 0.5  # -222

        xlim = mid_x - max_range, mid_x + max_range  # (42.0, 396.0)
        ylim = mid_y - max_range, mid_y + max_range  # (38.0, 392.0)
        zlim = mid_z - max_range, mid_z + max_range  # (38.0, 392.0)

        # reset x,y not (0,0) center
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_zlim(zlim)

        # plt.title(imgname, fontsize=14, fontweight='bold')

    if out_path:
        plt.savefig(out_path,
                    bbox_inches="tight",
                    # pad_inches=0.0
                    )

    if plt_show:
        plt.show()
    else:
        plt.close('all')


def plt_mask(mask):
    img_h, img_w = mask.shape
    plt.figure(figsize=(img_w / 100.0, img_h / 100.0))
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')
    plt.imshow(mask, cmap=plt.get_cmap('jet'))
    plt.show()


def plt_map(kp_map, image=None):
    """
    plt keypoint_map or paf_map in a heatmap way
    """
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    if image is not None:
        plt.imshow(image)
        img_h, img_w, _ = image.shape
        kp_map = cv2.resize(kp_map, dsize=(img_w, img_h))

    plt.imshow(kp_map, alpha=0.5, cmap=plt.get_cmap('jet'))
    plt.show()


def plt_kp_maps(kp_maps, joints_name, image=None):
    """
    plt keypoint_maps in a heatmap way
    """

    LEN = kp_maps.shape[0]
    joints_name.append('bg')

    cols = 5
    rows = int(math.ceil(LEN / cols))

    # use subplot to plt multi imgs
    f, axs = plt.subplots(rows, cols)
    f.set_size_inches((cols * 4, rows * 3))  # 4:3, corresponds to img aspect ratio

    if image is not None:
        img_h, img_w, _ = image.shape
        for i in range(LEN):
            ax = axs.flat[i]
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axis('off')
            ax.imshow(image)
            kp_map = cv2.resize(kp_maps[i], dsize=(img_w, img_h))
            ax.imshow(kp_map, alpha=0.5, cmap=plt.get_cmap('jet'))
            ax.set_title(joints_name[i])
    else:
        for i in range(LEN):
            axs.flat[i].imshow(kp_maps[i], alpha=0.5, cmap=plt.get_cmap('jet'))

    plt.show()


def plt_paf_vector(paf_map, image=None):
    """
    paf_map: limb paf_map, x,y
    """
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    U = paf_map[0] * -1  # (h,w)
    V = paf_map[1]

    if image is not None:
        plt.imshow(image, alpha=0.5)
        img_h, img_w, _ = image.shape
        U = cv2.resize(U, dsize=(img_w, img_h), interpolation=cv2.INTER_NEAREST)  # resize to image size
        V = cv2.resize(V, dsize=(img_w, img_h), interpolation=cv2.INTER_NEAREST)

    X, Y = np.meshgrid(np.arange(U.shape[1]), np.arange(U.shape[0]))  # w,h -> x,y
    M = np.zeros(U.shape, dtype=np.bool)
    M[U ** 2 + V ** 2 < 0.5 * 0.5] = True

    U = np.ma.masked_array(U, mask=M)
    V = np.ma.masked_array(V, mask=M)

    s = 10  # step
    plt.quiver(X[::s, ::s], Y[::s, ::s], U[::s, ::s], V[::s, ::s],
               scale=50, headaxislength=4, alpha=.5, width=0.001, color='r')
    plt.show()


def plt_sample(sample, joints_link):
    # image, keypts, mask
    # plt_2d_skeleton_MP(sample['image'], sample['multi_keypts'], joints_link)
    # plt_mask(sample['mask'])

    keypoint_maps, paf_maps = sample['keypoint_maps'], sample['paf_maps']

    # heatmap
    plt_map(1 - keypoint_maps[-1], sample['image'])  # last map
    # paf
    limb_id = 8  # R_elbow -> R_wrist
    plt_map(paf_maps[limb_id * 2], sample['image'])  # x
    plt_map(paf_maps[limb_id * 2 + 1], sample['image'])  # y
    plt_paf_vector(paf_maps[limb_id * 2:limb_id * 2 + 2, :, :], sample['image'])
