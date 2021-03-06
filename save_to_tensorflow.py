#!/usr/bin/env python
# -*- coding:utf-8 -*-
from keras.models import model_from_json
import tensorflow as tf
import os
import os.path as osp
from keras import backend as K


input_fld = "model/model_face.json"
weight_file = "model/model_face.h5"
num_output = 1
write_graph_def_ascii_flag = True
prefix_output_node_names_of_final_network = 'output_node'
output_graph_name = 'constant_graph_weights.pb'

if not os.path.exists("./pb"):
    os.mkdir("./pb")
output_fld =  'pb/tensorflow_model/'

if not os.path.isdir(output_fld):
    os.mkdir(output_fld)
weight_file_path = weight_file


K.set_learning_phase(0)
#net_model = load_model(input_fld,weight_file_path)
json_file = open(input_fld, 'r')
loaded_model_json = json_file.read()
json_file.close()
net_model = model_from_json(loaded_model_json)
# load weights into new model
net_model.load_weights("model/model_face.h5")

pred = [None]*num_output
pred_node_names = [None]*num_output
for i in range(num_output):
    pred_node_names[i] = prefix_output_node_names_of_final_network+str(i)
    pred[i] = tf.identity(net_model.output[i], name=pred_node_names[i])
print('output nodes names are: ', pred_node_names)


sess = K.get_session()

if write_graph_def_ascii_flag:
    f = 'only_the_graph_def.pb.ascii'
    tf.train.write_graph(sess.graph.as_graph_def(), output_fld, f, as_text=True)
    print('saved the graph definition in ascii format at: ', osp.join(output_fld, f))

from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), pred_node_names)
graph_io.write_graph(constant_graph, output_fld, output_graph_name, as_text=False)
print('saved the constant graph (ready for inference) at: ', osp.join(output_fld, output_graph_name))