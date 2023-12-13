# -*- coding: utf-8 -*-
"""project-Reimplementation_of_StyleCLIPDraw.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1doUe9woYNPK_yvOS4z_e61GJ0bBnHQws

# Introduction

**StyleCLIPDraw: Coupling Content and Style in Text-to-Drawing Synthesis**

<figure>
<img src="https://drive.google.com/uc?export=view&id=1yTLgvg2m4YxqGOEzWU4k2-6HVqsZ3u9F" alt="Comparing styled text-to-drawing results" width="80%" class="center">
<figcaption align="center">Comparing styled text-to-drawing results.

The baseline is formed by using CLIPDraw to convert the input text into an image, then performing Style Transfer. The StyleCLIPDraw couples style and content by generating the drawing using both the text and style simultaneously.</figcaption>
</figure>

> StyleCLIPDraw adds a style loss to the CLIPDraw text-to-drawing synthesis model to allow artistic control of the synthesized drawings in addition to control of the content via text. Whereas performing decoupled Style Transfer on a generated image only affects the texture. The proposed StyleCLIPDraw coupled approach is able to capture a style in both texture and shape, suggesting that the style of the drawing is coupled with the drawing process itself.

<br>

**StyleCLIPDraw:**
[Paper](https://arxiv.org/abs/2111.03133) &nbsp;
[Colab](https://colab.research.google.com/github/pschaldenbrand/StyleCLIPDraw/blob/master/Style_ClipDraw.ipynb) &nbsp;
[Code](https://github.com/pschaldenbrand/StyleCLIPDraw)

<br>

### Acknowledgement

StyleCLIPDraw is built off of CLIPDraw (Frans et al. 2021).

**CLIPDraw:**
[Paper](https://arxiv.org/abs/2106.14843) &nbsp;
[Colab](https://colab.research.google.com/github/kvfrans/clipdraw/blob/main/clipdraw.ipynb) &nbsp;
[Code](https://github.com/kvfrans/clipdraw)

# Architecture

The Bézier curve representation is converted into a raster image and is then used to compute two losses: One loss for aligning the content of the image with the user’s text prompt and the other for aligning style.

<figure>
<img src="https://drive.google.com/uc?export=view&id=1QRcvAzZ7vXe1zsshWmOwBnJTDnXl7vxf" alt="Comparing styled text-to-drawing results" width="100%">
<figcaption align="center">The StyleCLIPDraw model architecture.
</figcaption>
</figure>

<figure>
<img src="https://drive.google.com/uc?export=view&id=1Izj02kc_FlG3SccOFWJQf3jeTJjih-_X" alt="Comparing styled text-to-drawing results" width="40%" class="center">
<figcaption>The CLIPDraw algorithm. <br>
The Style Loss optimization step goes after Compute Loss step.
</figcaption>
</figure>

The drawing begins as randomized Bézier curves on a canvas and is optimized to fit the given style and text:

* The CLIPDraw produces drawings consisting of
a series of Bézier curves defined by a list of coordinates, a color, and an opacity.

* The brush strokes are rendered into a raster
image via differentiable model.


* The image is augmented to avoid finding shallow solutions to optimizing through the CLIP model.

* The text input and the augmented raster drawing are fed the the CLIP model and the difference in embeddings are compared using cosine distance to compute a loss that encourages the drawing to
fit the text input.

* The raster image and the style image are fed through early layers of the VGG-16 model (per the STROTSS style-transfer algorithm) and the difference in extracted features form the loss that encourages the drawings to fit the style of the style image.

# Implementation

As shown on architecure scheme the StyleCLIPDraw is a sum of CLIPDraw architecture and Style Loss optimization. There are two inputs: User Prompt (text) and Style Image.

The authors of the StyleCLIPDraw got all parts of CLIPDraw from it's original source.

Then they slightly modified the STROTSS style-transfer algorithm and implemented it into the CLIPDraw.

<br>

**STROSS - Style Transfer by Relaxed Optimal Transport and Self-Similarity:**
[Paper](https://arxiv.org/abs/1904.12785) &nbsp;
[Code](https://github.com/nkolkin13/STROTSS)

<figure>
<img src="https://drive.google.com/uc?export=view&id=1veAMc2IpEr64KGwek4cSBgPeERqwp0vM" alt="Comparing styled text-to-drawing results" width="100%" class="center">
<figcaption align="center">Examples of SCROTSS output for unconstrained (left) and guided (right) style transfer.

Images are arranged in order of content, output, style.</figcaption>
</figure>
<br>

As shown on outputs examples the StyleCLIPDraw not only applies the style onto images as do style transfer algorithms, but it also makes changes on the content of the drawing.

# Reimplementation

Since the work on StyleCLIPDraw was mainly about developing a Style Loss optimizer, while the authors got the ready CLIPDraw part from original source, I reimplemented the Style Loss part and did changes on data loadings and on some functions.

My reimplementation idea was not to use SCROTTS style-transfer algorithm for Style Loss, but try some other style transfer, where it does same thing - calculate a loss between content image and style image in order to make draw optimizations. For this purpose I used a Neural Style Transfer with Deep VGG-19 model relying on these sources:
[1](https://medium.com/@sashankpappu/style-transfer-using-pytorch-cb6225cf183e), [2](https://www.pluralsight.com/guides/artistic-neural-style-transfer-with-pytorch), [3](https://medium.com/@mirzezadeh.elvin/neural-style-transfer-with-deep-vgg-model-26b11ea06b7e), [4](https://www.youtube.com/watch?v=imX4kSKDY7s&t=979s). Also I added optimizers as in StyleCLIPDraw. On SCROTSS there was used VGG-16 model for Feature Extractions.
<br>

Since we have only two inputs, user prompt in text and style image, as a content image we get a raster image from CLIPDraw. The raster image is a pixel-based image rendered by [diffvg](https://github.com/BachiLi/diffvg) function. The diffvg gets as a parameters canvas width, height and Bézier curves values which are units of vector based graphics and diffvg transforms them into pixel-based graphics, i.e. to image, so in such way we get the content image.

<figure>
<img src="https://drive.google.com/uc?export=view&id=1eRHOc0q4JzGQHwpwNuYSCRezmckh9_0R" alt="Comparing styled text-to-drawing results" width="80%" class="center">
<figcaption align="center">Neural Style Transfer with Deep VGG-19 model.</figcaption>
</figure>

<br>

> Pre Installation - from CLIPDraw source

> Check GPU - checking runtime type

> Imports and Image Functions - all necessary imports and functions for image manipulation

> Load CLIP and text_features - instead of putting a cumbersome buil-in text as it was on original source I load the dataset from CIFAR-100, also prepare a text input and initialize text_features variable

> Neural Style Transfer and CLIPDraw Functions - functions from Neural Style Transfer and CLIPDraw sources

> clip_draw() - from CLIPDraw source, in order to show the  differences between outputs from CLIPDraw without style optimization and output from StyleCLIPDraw

> style_clip_draw() - added the reimplemented Style Transfer and Style Loss parts, CLIPDraw parts from original source

> Outputs - testing how does it work by showing the intermediate results and final result

Directions


1. Click "Connect" in the top right corner
2. Runtime -> Change runtime type -> Hardware accelerator -> GPU
3. Click the run button on "Pre Installation". This will install dependencies, it may take a while.
4. **Important:** Runtime -> Restart Runtime
5. Run the imports and function definition sections.
  - **Important:** The "Imports and Notebook Utilities" cell will print which GPU you have been assigned.  This notebook needs to be run with a T4, P4, P100, or V100 GPU (**K80 will not work**, unfortunately). You may have to restart the machine a few times until you get assigned a valid GPU (Runtime -> manage sessions -> terminate the session -> re-connect to new session).
6. Run the `style_clip_draw()` function with your own parameters. See the last few cells for examples
"""

# Commented out IPython magic to ensure Python compatibility.
#@title Pre Installation {vertical-output: true}

import subprocess

CUDA_version = [s for s in subprocess.check_output(["nvcc", "--version"]).decode("UTF-8").split(", ") if s.startswith("release")][0].split(" ")[-1]
print("CUDA version:", CUDA_version)

if CUDA_version == "10.0":
    torch_version_suffix = "+cu100"
elif CUDA_version == "10.1":
    torch_version_suffix = "+cu101"
elif CUDA_version == "10.2":
    torch_version_suffix = ""
else:
    torch_version_suffix = "+cu110"

# !pip install torch==1.7.1{torch_version_suffix} torchvision==0.8.2{torch_version_suffix} -f https://download.pytorch.org/whl/torch_stable.html ftfy regex
# %cd /content/
!pip install svgwrite
!pip install svgpathtools
!pip install cssutils
!pip install numba
!pip install torch-tools
!pip install visdom

!git clone https://github.com/BachiLi/diffvg
# %cd diffvg
# !ls
!git submodule update --init --recursive
!python setup.py install

!pip install ftfy regex tqdm
!pip install git+https://github.com/openai/CLIP.git --no-deps

#@title Check GPU {vertical-output: true}
!nvidia-smi -L

print('\nThe GPU must be a T4, P4, P100, or V100 GPU (K80 will not work, unfortunately)')
print('If the valid GPU is not assigned, please restart the machine until a valid GPU is assigned:')
print('Runtime -> manage sessions -> terminate the session -> start a new session')
print('If GPU is not available, the code works fine on CPU as well')

#@title Imports and Image Functions {vertical-output: true}

import os
import io
import requests
import random

import numpy as np
import PIL.Image
import matplotlib.pyplot as plt

import torch
from torchvision import transforms, models
from torchvision.datasets import CIFAR100

import clip
import pydiffvg

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

pydiffvg.set_print_timing(False)
pydiffvg.set_use_gpu(torch.cuda.is_available())
pydiffvg.set_device(device)


# Load in and transform an image, making sure the image is <= 400 pixels in the x-y dims
def load_image(img_path, max_size=400, shape=None):

    if img_path.startswith(('http:', 'https:')):
        r = requests.get(img_path)
        f = io.BytesIO(r.content)
    else:
        f = img_path

    image = PIL.Image.open(f).convert('RGB')

    # large images will slow down processing
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)

    if shape is not None:
        size = shape

    in_transform = transforms.Compose([
                        transforms.Resize(size),
                        transforms.ToTensor(),
                        transforms.Normalize((0.485, 0.456, 0.406),
                                             (0.229, 0.224, 0.225))])

    # discard the transparent, alpha channel (that's the :3) and add the batch dimension
    image = in_transform(image)[:3,:,:].unsqueeze(0)

    return image

# converting tensor to a NumPy image for display
def im_convert(tensor):
    """ Display a tensor as an image. """

    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1,2,0)
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image = image.clip(0, 1)
    return image

def clean_img(img):
    img = np.transpose(img, (1, 2, 0))
    img = np.clip(img, 0, 1)
    img = np.uint8(img * 254)
    return img

#@title Load CLIP and text_features {vertical-output: true}

# Load the model
model, preprocess = clip.load('ViT-B/32', device=device, jit=False)
# available models: ['RN50', 'RN101', 'RN50x4', 'RN50x16', 'ViT-B/32', 'ViT-B/16']

# Download CIFAR100 dataset
cifar100 = CIFAR100(os.path.expanduser("~/.cache"), transform=preprocess, download=True)

# Prepare text inputs
text_descriptions = [f"This is a drawing of a {label}" for label in cifar100.classes]
text_inputs = torch.cat([clip.tokenize(text_descriptions)]).to(device)

# Calculate text features
with torch.no_grad():
    text_features = model.encode_text(text_inputs)

#@title Neural Style Transfer and CLIPDraw Functions {vertical-output: true}

# Neural Style Transfer

# getting VGG19 feature extraction
vgg = models.vgg19(pretrained=True).features
for param in vgg.parameters():
    param.requires_grad_(False)

# move the model to GPU, if available
vgg.to(device)

# weights for each style layer
style_weights = {'conv1_1': 1.5,
                 'conv2_1': 0.80,
                 'conv3_1': 0.25,
                 'conv4_1': 0.25,
                 'conv5_1': 0.25}

content_weight = 1e-2 # alpha
style_weight = 1e9 # beta

def get_features(image, layers=None):
    """ Run an image forward through a vgg and get the features for
        a set of layers. Default layers are for VGGNet matching Gatys et al (2016)
    """

    if layers is None:
        layers = {'0': 'conv1_1',
                  '5': 'conv2_1',
                  '10': 'conv3_1',
                  '19': 'conv4_1',
                  '21': 'conv4_2',  ## content representation
                  '28': 'conv5_1'}

    features = {}
    x = image

    for name, layer in vgg._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x

    return features

def gram_matrix(tensor):
    """ Calculate the Gram Matrix of a given tensor
        Gram Matrix: https://en.wikipedia.org/wiki/Gramian_matrix
    """

    # get the batch_size, depth, height, and width of the Tensor
    b, d, h, w = tensor.size()

    # reshape so we're multiplying the features for each channel
    tensor = tensor.view(d, h * w)

    # calculate the gram matrix
    gram = torch.mm(tensor, tensor.t())

    return gram



# CLIPDraw

def initialize_curves(num_paths, canvas_width, canvas_height):
    shapes = []
    shape_groups = []
    for i in range(num_paths):
        num_segments = random.randint(1, 3)
        num_control_points = torch.zeros(num_segments, dtype = torch.int32) + 2
        points = []
        p0 = (random.random(), random.random())
        points.append(p0)
        for j in range(num_segments):
            radius = 0.1
            p1 = (p0[0] + radius * (random.random() - 0.5), p0[1] + radius * (random.random() - 0.5))
            p2 = (p1[0] + radius * (random.random() - 0.5), p1[1] + radius * (random.random() - 0.5))
            p3 = (p2[0] + radius * (random.random() - 0.5), p2[1] + radius * (random.random() - 0.5))
            points.append(p1)
            points.append(p2)
            points.append(p3)
            p0 = p3
        points = torch.tensor(points)
        points[:, 0] *= canvas_width
        points[:, 1] *= canvas_height
        path = pydiffvg.Path(num_control_points = num_control_points, points = points, stroke_width = torch.tensor(1.0), is_closed = False)
        shapes.append(path)
        path_group = pydiffvg.ShapeGroup(shape_ids = torch.tensor([len(shapes) - 1]), fill_color = None, stroke_color = torch.tensor([random.random(), random.random(), random.random(), random.random()]))
        shape_groups.append(path_group)
    return shapes, shape_groups

# for image augmentation step
def get_image_augmentation(use_normalized_clip):
    augment_trans = transforms.Compose([
        transforms.RandomPerspective(fill=1, p=1, distortion_scale=0.5),
        transforms.RandomResizedCrop(224, scale=(0.7,0.9)),
    ])

    if use_normalized_clip:
        augment_trans = transforms.Compose([
        transforms.RandomPerspective(fill=1, p=1, distortion_scale=0.5),
        transforms.RandomResizedCrop(224, scale=(0.7,0.9)),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711))
    ])
    return augment_trans

# rendering Bezier curves to pixel-based image
def render_drawing(shapes, shape_groups, canvas_width, canvas_height, n_iter):
    scene_args = pydiffvg.RenderFunction.serialize_scene(canvas_width, canvas_height, shapes, shape_groups)
    render = pydiffvg.RenderFunction.apply
    img = render(canvas_width, canvas_height, 2, 2, n_iter, None, *scene_args)
    img = img[:, :, 3:4] * img[:, :, :3] + torch.ones(img.shape[0], img.shape[1], 3, device = pydiffvg.get_device()) * (1 - img[:, :, 3:4])
    img = img[:, :, :3]
    img = img.unsqueeze(0)
    img = img.permute(0, 3, 1, 2) # NHWC -> NCHW
    return img

#@title clip_draw() { form-width: "10%" }

def clip_draw(prompt, num_paths=256, num_iter=100, max_width=50,\
                    num_augs=4, neg_prompt=None, neg_prompt_2=None,\
                    use_normalized_clip=False):
    '''
    Perform CLIPDraw using a given text prompt
    args:
        prompt (str) : Text prompt to draw
    kwargs:
        num_paths (int) : Number of brush strokes
        num_iter(int) : Number of optimization iterations
        max_width(float) : Maximum width of a brush stroke in pixels
        num_augs(int) : Number of image augmentations
        neg_prompt(str) : Negative prompt. None if you don't want it
        neg_prompt_2(str) : Negative prompt. None if you don't want it
        use_normalized_clip(bool)
    return
        np.ndarray(drawn image without style)
    '''
    text_input = clip.tokenize(prompt).to(device)

    if neg_prompt is not None: text_input_neg1 = clip.tokenize(neg_prompt).to(device)
    if neg_prompt_2 is not None: text_input_neg2 = clip.tokenize(neg_prompt_2).to(device)

    # Calculate features
    with torch.no_grad():
        text_features = model.encode_text(text_input)
        if neg_prompt is not None: text_features_neg1 = model.encode_text(text_input_neg1)
        if neg_prompt_2 is not None: text_features_neg2 = model.encode_text(text_input_neg2)

    canvas_width, canvas_height = 224, 224

    # Initialize Random Curves
    shapes, shape_groups = initialize_curves(num_paths, canvas_width, canvas_height)

    # Image Augmentation Transformation
    augment_trans = get_image_augmentation(use_normalized_clip)

    points_vars = []
    stroke_width_vars = []
    color_vars = []
    for path in shapes:
        path.points.requires_grad = True
        points_vars.append(path.points)
        path.stroke_width.requires_grad = True
        stroke_width_vars.append(path.stroke_width)
    for group in shape_groups:
        group.stroke_color.requires_grad = True
        color_vars.append(group.stroke_color)

    # Optimizers
    points_optim = torch.optim.Adam(points_vars, lr=1.0)
    width_optim = torch.optim.Adam(stroke_width_vars, lr=0.1)
    color_optim = torch.optim.Adam(color_vars, lr=0.01)

    for t in range(num_iter):

        points_optim.zero_grad()
        width_optim.zero_grad()
        color_optim.zero_grad()

        img = render_drawing(shapes, shape_groups, canvas_width, canvas_height, t)

        loss = 0
        img_augs = []
        for n in range(num_augs):
            img_augs.append(augment_trans(img))
        im_batch = torch.cat(img_augs)
        image_features = model.encode_image(im_batch)
        for n in range(num_augs):
            loss -= torch.cosine_similarity(text_features, image_features[n:n+1], dim=1)
            if neg_prompt is not None: loss += torch.cosine_similarity(text_features_neg1, image_features[n:n+1], dim=1) * 0.3
            if neg_prompt_2 is not None: loss += torch.cosine_similarity(text_features_neg2, image_features[n:n+1], dim=1) * 0.3

        loss.backward()
        points_optim.step()
        width_optim.step()
        color_optim.step()

        for path in shapes:
            path.stroke_width.data.clamp_(1.0, max_width)
        for group in shape_groups:
            group.stroke_color.data.clamp_(0.0, 1.0)

    return img

#@title style_clip_draw() { form-width: "10%" }


def style_clip_draw(prompt, style_path, \
                    num_paths=256, num_iter=200, max_width=50,\
                    num_augs=4, style_opt_freq=5, style_opt_iter=20,
                    neg_prompt=None, neg_prompt_2=None,\
                    use_normalized_clip=False):
    '''
    Perform StyleCLIPDraw using a given text prompt and style image
    args:
        prompt (str) : Text prompt to draw
        style_path(str) : Style image path or url
    kwargs:
        num_paths (int) : Number of brush strokes
        num_iter(int) : Number of optimization iterations
        max_width(float) : Maximum width of a brush stroke in pixels
        num_augs(int) : Number of image augmentations
        style_opt_freq(int) : How often to do style optimization. Low value is high frequency
        style_opt_iter(int) : How many iterations to do in the style optimization loop
        neg_prompt(str) : Negative prompt. None if you don't want it
        neg_prompt_2(str) : Negative prompt. None if you don't want it
        use_normalized_clip(bool)
    return
        np.ndarray(style image, drawn image)
    '''
    text_input = clip.tokenize(prompt).to(device)

    if neg_prompt is not None: text_input_neg1 = clip.tokenize(neg_prompt).to(device)
    if neg_prompt_2 is not None: text_input_neg2 = clip.tokenize(neg_prompt_2).to(device)

    # Calculate features
    with torch.no_grad():
        text_features = model.encode_text(text_input)
        if neg_prompt is not None: text_features_neg1 = model.encode_text(text_input_neg1)
        if neg_prompt_2 is not None: text_features_neg2 = model.encode_text(text_input_neg2)

    canvas_width, canvas_height = 224, 224

    # Initialize Random Curves
    shapes, shape_groups = initialize_curves(num_paths, canvas_width, canvas_height)

    # Image Augmentation Transformation
    augment_trans = get_image_augmentation(use_normalized_clip)

    points_vars = []
    stroke_width_vars = []
    color_vars = []
    for path in shapes:
        path.points.requires_grad = True
        points_vars.append(path.points)
        path.stroke_width.requires_grad = True
        stroke_width_vars.append(path.stroke_width)
    for group in shape_groups:
        group.stroke_color.requires_grad = True
        color_vars.append(group.stroke_color)

    # Optimizers
    points_optim = torch.optim.Adam(points_vars, lr=1.0)
    width_optim = torch.optim.Adam(stroke_width_vars, lr=0.1)
    color_optim = torch.optim.Adam(color_vars, lr=0.01)

    # points_vars = [l.data.requires_grad_() for l in points_vars]
    points_optim_style = torch.optim.RMSprop(points_vars, lr=0.1)
    width_optim_style = torch.optim.RMSprop(stroke_width_vars, lr=0.1)
    color_optim_style = torch.optim.RMSprop(color_vars, lr=0.01)


    # loading style image
    style = load_image(style_path, shape=[canvas_width, canvas_height]).to(device)

    # getting style features
    style_features = get_features(style)

    # calculate the gram matrices for each layer of our style representation
    style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

    points_optim_style = torch.optim.RMSprop(points_vars, lr=0.1)
    width_optim_style = torch.optim.RMSprop(stroke_width_vars, lr=0.1)
    color_optim_style = torch.optim.RMSprop(color_vars, lr=0.01)

    # points_optim_style = torch.optim.Adam(points_vars, lr=0.1)
    # width_optim_style = torch.optim.Adam(stroke_width_vars, lr=0.1)
    # color_optim_style = torch.optim.Adam(color_vars, lr=0.01)


    # Run the main optimization loop
    for t in range(num_iter):

        points_optim.zero_grad()
        width_optim.zero_grad()
        color_optim.zero_grad()

        img = render_drawing(shapes, shape_groups, canvas_width, canvas_height, t)
        # img = render_drawing(shapes, shape_groups, canvas_width, canvas_height, t, save=(t % 5 == 0))

        # showing intermediate state of the rendering, while optimizing curves parameters
        print('LOSS ITER: ', t+1)
        plt.imshow(clean_img(img.detach().cpu().numpy()[0]))
        plt.show()

        loss = 0
        img_augs = []
        for n in range(num_augs):
            img_augs.append(augment_trans(img))
        im_batch = torch.cat(img_augs)
        image_features = model.encode_image(im_batch)
        for n in range(num_augs):
            loss -= torch.cosine_similarity(text_features, image_features[n:n+1], dim=1)
            if neg_prompt is not None: loss += torch.cosine_similarity(text_features_neg1, image_features[n:n+1], dim=1) * 0.3
            if neg_prompt_2 is not None: loss += torch.cosine_similarity(text_features_neg2, image_features[n:n+1], dim=1) * 0.3

        loss.backward()
        points_optim.step()
        width_optim.step()
        color_optim.step()

        # reimplementation of Style Transfer optimization
        if t%style_opt_freq == 0 or (t == num_iter-1):

            img = render_drawing(shapes, shape_groups, canvas_width, canvas_height, t)
            content_features = get_features(img)

            # inner loop, iteration for style optimization
            for it in range(style_opt_iter):

                # adding optimizers for curves style
                points_optim_style.zero_grad()
                width_optim_style.zero_grad()
                color_optim_style.zero_grad()
                # optimizer.zero_grad()

                img = render_drawing(shapes, shape_groups, canvas_width, canvas_height, t)

                # showing intermediate state of the renderings, while optimizating style features
                print('LOSS ITER: ', t+1, ' ->  STYLE LOSS ITER: ', it+1)
                plt.imshow(clean_img(img.detach().cpu().numpy()[0]))
                plt.show()

                # getting features of content image
                target_features = get_features(img)

                #calculating content loss by formula
                content_loss = torch.mean((target_features["conv4_2"] - content_features["conv4_2"]) ** 2)

                style_loss = 0

                # iterate through each style layer and add to the style loss
                for layer in style_weights:

                    # get the content style representation for the layer
                    target_feature = target_features[layer]

                    #getting batch size, depth, height, width of content image features
                    b, d, h, w = target_feature.shape

                    target_gram = gram_matrix(target_feature)
                    style_gram = style_grams[layer]

                    # the style loss for one layer, weighted appropriately
                    layer_style_loss = style_weights[layer] * torch.mean((target_gram - style_gram) ** 2)

                    style_loss += layer_style_loss / (d * h * w)

                # calculate the total loss
                total_loss = content_weight * content_loss + style_weight * style_loss

                # retain_graph=True is necessary to add, since there are two backwards
                total_loss.backward(retain_graph=True)

                # updatimg redering image
                points_optim_style.step()
                width_optim_style.step()
                color_optim_style.step()
                # optimizer.step()

            for path in shapes:
                path.stroke_width.data.clamp_(1.0, max_width)
            for group in shape_groups:
                group.stroke_color.data.clamp_(0.0, 1.0)

    return style, img

"""# Outputs

The outputs qualities depend on number of overall iterations and number of style iteration for optimizations, and also from selected style image. In order to get more quality drawn output, we need to increase the iteration numbers. As it is shown, the drawn output images inherit the style features of a given image, while also affecting on shape, size and location of the objects. According to result outputs we can assume that the reimplemented style optimization performs correctly and satisfies our requests.

<br>

Some experiment results:
* num_iter(int): Number of optimization iterations
* style_opt_iter(int): How many iterations to do in the style optimization loop
* style_opt_freq(int): How often to do style optimization. Low value is high frequency

<br>

num_iter = 100, style_opt_iter = 10, style_opt_freq = 5

<br>

Test 1:
<figure>
<img src="https://drive.google.com/uc?export=view&id=1RJe-eYfzQq0e3cV5kFl6w1VewwY46pfU" width="100%" class="center">
<figcaption align="center">A man is watching TV
<br>
As we can see reimplemented StyleCLIPDraw got style images features, while CLIPDraw chose random colors. We can also see square boxes which indicates that they are TVs and man is sitting on sofa and watching TVs.</figcaption>
</figure>

<br>

Test 2:
<figure>
<img src="https://drive.google.com/uc?export=view&id=1HSHcMj_bOVnnVJqpsXNQ1CjY8xbjsUAC" width="100%" class="center">
<figcaption align="center">A man is walking the dog
<br>
As we can see reimplemented StyleCLIPDraw applies white and dark colors on output. If we increase iteration numbers we would in all posibilities get more matching outputs. We can see on output image a man walking and near him a dog.</figcaption>
</figure>

<br>

Test 3:
<figure>
<img src="https://drive.google.com/uc?export=view&id=1IFquVxmoTmTchgdjzVGloARSezFBDWpv" width="100%" class="center">
<figcaption align="center">A horse eating a cupcake
<br>
The output from StyleCLIPDraw inherits the color set of the style image. It is interesting to see that on output image blue color covers most of the area as in style image. We can see a cupcake and some figure with protruding head and white ears sitting on table which we can assume it as a horse.</figcaption>
</figure>

<br>

Test 4:
<figure>
<img src="https://drive.google.com/uc?export=view&id=19KHVzqlI92ilKbNkmw2Gcjrqqtv1lhB1" width="100%" class="center">
<figcaption align="center">A girl riding a motocycle
<br>
On the output image we can see a figure of a girl with yellow long hair in red pants, she is sitting on a vehile, which we can assume as a motocycle. Thanks to the style optimization the drawn image is more detailed compare to the outputs without style optimization.</figcaption>
</figure>

<br>

Test 5:
<figure>
<img src="https://drive.google.com/uc?export=view&id=1JUkmHpn044U08NGcDGLSTeKSveOmri5v" width="100%" class="center">
<figcaption align="center">The trees across the street
<br>
On the output image we can see a big tree in the center and some other trees around. On drawn outputs we can see how they also inherit the texture of the style images. In this example the trees have more defined branches just like a rough skin of the lizard.</figcaption>
</figure>

<br>

Test 6:
<figure>
<img src="https://drive.google.com/uc?export=view&id=19z-ulb3NDO9DlrHZ0K7qdb20C0fJFwP0" width="100%" class="center">
<figcaption align="center">A group of people at the meeting
<br>
On the output image we can see figures of people sitting and standind around the white table. We can assume that it as a meeting. The color set of the output image is matching to style image.</figcaption>
</figure>

Test 7:
<figure>
<img src="https://drive.google.com/uc?export=view&id=1fipsta1YWznJEdhoWFyIe3hbRdBr2Huu" width="100%" class="center">
<figcaption align="center">A bridge over the lake
<br>
We can see a bridge structure and blue water. From output examples we can say that style optimization not only draws according to color set of the style image, but also fills the drawn objects in corresponding colors, while outputs from CLIPDraw are not colorized.
</figcaption>
</figure>

<br>

Test 8:
<figure>
<img src="https://drive.google.com/uc?export=view&id=1whc1Br5sttA1YQFo-hhQOSPNOMjgb7gv" width="100%" class="center">
<figcaption align="center">A bottle of juice
<br>
The are just two distinguishable colors on the style image, orange and white, but on output image we can see some other colors in drawing the style optimization added in order to make a shape of objects. We can see some bottles with caps on them, we can assume them as bottles of juice.
</figcaption>
</figure>

<br>



"""

#@title Test-1 {vertical-output: true}

prompt = 'A man is watching TV'
style = 'https://raw.githubusercontent.com/pschaldenbrand/StyleCLIPDraw/master/images/fruit.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-2 {vertical-output: true}

prompt = 'A man is walking the dog'
style = 'https://cdn.pixabay.com/photo/2022/01/20/05/31/birds-6951496_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-3 {vertical-output: true}

prompt = 'A horse eating a cupcake'
style = 'https://cdn.pixabay.com/photo/2020/11/27/06/58/cat-5781057_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-4 {vertical-output: true}

prompt = 'A girl riding a motocycle'
style = 'https://cdn.pixabay.com/photo/2018/08/12/16/59/parrot-3601194_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-5 {vertical-output: true}

prompt = 'The trees across the street'
style = 'https://cdn.pixabay.com/photo/2022/01/28/00/21/dragon-6973456_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-6 {vertical-output: true}

prompt = 'A group of people at the meeting'
style = 'https://cdn.pixabay.com/photo/2021/11/03/13/19/background-6765817_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-7 {vertical-output: true}

prompt = 'A bridge over the lake'
style = 'https://cdn.pixabay.com/photo/2018/06/13/18/20/waves-3473335_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)

#@title Test-8 {vertical-output: true}

prompt = 'A bottle of juice'
style = 'https://cdn.pixabay.com/photo/2021/08/03/07/03/orange-6518675_960_720.jpg'
num_iter = 100
style_opt_iter = 10
style_opt_freq = 5

style, scd_img = style_clip_draw(prompt, style, num_iter=num_iter, style_opt_freq=style_opt_freq, style_opt_iter=style_opt_iter)

cd_img = clip_draw(prompt, num_iter=num_iter)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 20))
# content and style imgs side-by-side

ax1.imshow(clean_img(cd_img.detach().cpu().numpy()[0]))
ax1.set_title("CLIPDraw image", fontsize = 20)

ax2.imshow(im_convert(style))
ax2.set_title("Style image", fontsize = 20)

ax3.imshow(clean_img(scd_img.detach().cpu().numpy()[0]))
ax3.set_title("StyleCLIPDraw image", fontsize = 20)