import tensorflow as tf

# callback function to stop training

class StopTraining(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if logs.get('acc') > 0.998:
            print("\n Reached 99.8% accuracy, so cancelling training !")
            self.model.stop_training = True


def train_mnist_conv():

    callbacks = StopTraining
    mnist = tf.keras.datasets.mnist
    (training_images, training_labels), (test_images, test_labels) = mnist.load_data()

    training_images = training_images.reshape(60000, 28, 28, 1)
    test_images = test_images.reshape(10000, 28, 28, 1)

    # Normalizing List
    training_images = training_images / 255.0
    test_images = test_images / 255.0

    # Define model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    # Train Model
    results = model.fit(training_images, training_labels, epochs=10, callbacks=[callbacks])
    trainAccuracy = results.history['acc'][-1]
    print("Training Accuracy: {}".format(trainAccuracy))

    # Evaluate the model on the Test data (Unseen Data)
    loss, testAccuracy = model.evaluate(test_images, test_labels)
    print("Loss: {}, Accuracy: {}".format(loss, testAccuracy))
    print("Difference in accuracy for training and test data is: {0:.2f} %".format((trainAccuracy - testAccuracy) * 100))



train_mnist_conv()
