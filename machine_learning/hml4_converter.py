import hls4ml
config = hls4ml.utils.config_from_keras_model(model, granularity='model')
hls_model = hls4ml.converters.convert_from_keras_model(model, hls_config=config, output_dir='hls4ml_mnist')
hls_model.compile()
