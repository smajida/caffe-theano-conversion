def parse_model_def(prototxt_path):
	f = open(prototxt_path)
	full = ''
	for line in f:
		full += line.rstrip('\n') + ' '

	# split on "layers"
	split = full.split('layers')
	
	# get input dimension
	input_splits = split[1].split()
	input_dims = []
	last_idx=0
	while(True):
		try:
			idx = input_splits.index('input_dim:', last_idx+1)
			input_dims.append(int(input_splits[idx+1]))
			last_idx=idx
		except:
			break

	# now go thru layers
	layers= []
	for layer_string in split[2:]:
		lsplit = layer_string.split()
		params = {}
		params['name'] = find_params('name',lsplit)
		params['type'] = find_params('type',lsplit)

		if params['type'] == 'CONVOLUTION':
			params['num_output'] = find_params('num_output', lsplit)
			params['pad'] = find_params('pad',lsplit)
			params['stride'] = find_params('stride',lsplit)
			params['kernel_size'] = find_params('kernel_size',lsplit)

		elif params['type'] == 'INNER_PRODUCT':
			params['num_output'] = find_params('num_output',lsplit)

		elif params['type'] == 'DROPOUT':
			params['dropout_ratio'] = find_params('dropout_ratio',lsplit)
		elif params['type'] == 'POOLING':
			params['pool'] = find_params('pool',lsplit)
			params['kernel_size'] = find_params('kernel_size',lsplit)
			params['stride'] = find_params('stride',lsplit)

		elif params['type'] == 'LRN':
			params['local_size'] = find_params('local_size', lsplit, default=5)
			params['alpha'] = find_params('alpha', lsplit, default=1)
			params['beta'] = find_params('beta', lsplit, default=5)

		else:
			raise Exception ("no type %s" % params['type'])


		layers.append(params)

	return input_dims, layers


def find_params(string, lsplit, default='DEFAULT'):
	try:
		idx = lsplit.index(string+':')
		return lsplit[idx+1].rstrip('"').lstrip('"')
	except:
		return default

if __name__ == '__main__':
	split = parse_model_def('VGG_ILSVRC_16_layers_deploy.prototxt')
