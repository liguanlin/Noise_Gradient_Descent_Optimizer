import tensorflow as tf
with_l2_norm=True
max_grad_norm=5.0
mean_=0.0
stddev_=1.0
update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
with tf.control_dependencies(update_ops):
	opt=tf.train.GradientDescentOptimizer(learning_rate)
	grads_and_vars = opt.compute_gradients(loss)
	if with_l2_norm:
  		noise_grads_and_vars=[(tf.squeeze(tf.clip_by_global_norm([gv[0]],max_grad_norm)[0],axis=0)+tf.nn.l2_normalize(tf.random_normal(gv[0].shape.as_list(),mean_,stddev_),dim=0),gv[1]) for gv in grads_and_vars]
  	else:
		noise_grads_and_vars=[(tf.squeeze(tf.clip_by_global_norm([gv[0]],max_grad_norm)[0],axis=0)+tf.random_normal(gv[0].shape.as_list(),mean_,stddev_),gv[1]) for gv in grads_and_vars]
	train_step_key_pred_net = opt.apply_gradients(noise_grads_and_vars)
	for var in tf.trainable_variables():
		tf.summary.histogram(var.name, var)
	for grad, var in noise_grads_and_vars:
		tf.summary.histogram(var.name + '/gradient', grad)
	
