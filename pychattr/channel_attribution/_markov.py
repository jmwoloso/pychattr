"""
Contains the model-fitting logic used for the Markov model.
"""
import tensorflow as tf
# use eager execution for easier debugging
tfe = tf.contrib.eager
use_tf_eager = True

import tensorflow_probability as tfp
tfd = tfp.distributions
tfb = tfp.bijectors


if use_tf_eager:
    try:
        tf.enable_eager_execution()
        print("Running TF Eager Execution.")
    except:
        print("Running Without TF Eager Execution.")

def _evaluate(tensors):
    """Evaluates Tensor or EagorTensor to Numpy ndarrays"""
    if tf.executing_eagerly():
        return tf.contrib.framework.nest.pack_sequence_as(
            tensors,
            [t.numpy() if tf.contrib.framework.is_tensor(t) else t
             for t in tf.contrib.framework.nest.flatten(tensors)]
        )
    return sess.run(tensors)


def _session_options(enable_gpu_ram_resizing=True, enable_xla=False):
    """Make use of GPUs if available."""
    config = tf.ConfigProto()
    config.log_device_placement=True
    if enable_gpu_ram_resizing:
        config.gpu_options.allow_growth=True
    if enable_xla:
        config.graph_options.optimizer_options.global_jit_level = (
            tf.OptimizerOptions.ON_1
        )
    return config


def _reset_sess(config=None):
    """Convenience function to create TF graph & session or reset
    them."""
    if config is None:
        config = session_options(enable_gpu_ram_resizing=True,
                                 enable_xla=False)
    global sess
    tf.reset_default_graph()
    try:
        sess.close()
    except:
        pass
    sess = tf.InteractiveSession(config=config)
_reset_sess()


def fit_markov():
    """Markov attribution model."""
    pass


