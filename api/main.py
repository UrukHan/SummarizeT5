import tensorflow as tf
import tensorflow_text
from fastapi import FastAPI
from pydantic import BaseModel

class UserRequestIn(BaseModel):
    input_text: str

class PredictionOut(BaseModel):
    output_text: str

saved_model_path = 'model'

def load_predict_fn(model_path):
    if tf.executing_eagerly():
        print("Loading SavedModel in eager mode.")
        imported = tf.saved_model.load(model_path, ["serve"])
        return lambda x: imported.signatures['serving_default'](tf.constant(x))['outputs'].numpy()
    else:
        print("Loading SavedModel in tf 1.x graph mode.")
        tf.compat.v1.reset_default_graph()
        sess = tf.compat.v1.Session()
        meta_graph_def = tf.compat.v1.saved_model.load(sess, ["serve"], model_path)
        signature_def = meta_graph_def.signature_def["serving_default"]
        return lambda x: sess.run(
            fetches=signature_def.outputs["outputs"].name, 
            feed_dict={signature_def.inputs["input"].name: x}
        )

def prediction(inp):
    return predict_fn([inp])[0].decode('utf-8')

predict_fn = load_predict_fn(saved_model_path)

app = FastAPI()

@app.get("/health_check")
def health_check():
    return {"code": 200, "status": "OK"}

@app.post("/api/predict", response_model=PredictionOut)
async def answer(user_request: UserRequestIn):
    input_text = user_request.input_text
    output_text = prediction(input_text)
    return {'output_text': output_text}



