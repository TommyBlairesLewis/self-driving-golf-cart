#
# training script
# for training deep learning models
# By Neil Nie
# (c) Yongyang Nie, 2018. All Rights Reserved
# Contact: contact@neilnie.com
#

import numpy as np
from models import utils as utils, configs as configs
import models.models as models
import matplotlib.pyplot as plt
from models.ConvLSTM import ConvLSTM


validation = True
visualize = False


def train(data_type="UDAT", model_type="Comma", load_weights=False, steps=5000, epochs=5, validation=False):

    # --------- check for model type  -------------
    if model_type == "comma":
        model = models.commaai_model()
    elif model_type == "nvidia":
        model = models.nvidia_model()
    elif model_type == "rambo":
        model = models.create_rambo_model()
    else:
        raise Exception("Unknown model type: " + model_type + ". Please enter a valid model type")

    # --------- check for dataset type ------------
    if data_type == "UDAT":
        labels = utils.preprocess_udacity_dataset(configs.dir, configs.dir2)
        training_gen = utils.udacity_batch_generator(labels, 8, True)
    elif data_type == "SELF":
        labels = utils.process_self_dataset(configs.dataset_dirs)
        training_gen = utils.self_batch_generator(labels, 8, True)
    else:
        raise Exception('Please enter a valid dataset type')

    print("data length {}".format(len(labels)))

    # -------- create the network or load weights -----
    if load_weights:
        model.load_weights(configs.model_path)
    model.summary()

    if visualize:
        images, steerings = next(training_gen)
        for i in range(len(images)):
            img = images[i]
            plt.imshow(np.array(img, dtype=np.uint8))
            plt.show()

    if validation:
        val_labels = utils.process_self_dataset([configs.val_dir])
        validation_gen = utils.self_batch_generator(val_labels, 8, False)

        model.fit_generator(training_gen, steps_per_epoch=steps, epochs=epochs, verbose=1, validation_data=validation_gen, validation_steps=800)
    else:
        model.fit_generator(training_gen, steps_per_epoch=steps, epochs=epochs, verbose=1)

    # standard model naming scheme
    # "[purpose]-[model type]-[dataset used]-[version].h5"
    # example:
    #         "str-cai-self-v1.h5"

    model.save('str-cai-self-v4.h5')


def train_conv_lstm():

    graph = ConvLSTM()
    graph.train(graph=graph.graph, saver=graph.saver)


if __name__ == "__main__":

    # train(data_type="SELF", model_type="comma", epochs=5, load_weights=True, validation=True)
    train_conv_lstm()