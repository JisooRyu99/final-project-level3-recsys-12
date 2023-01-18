import sys

sys.path.append("../")

import pandas as pd
from torch.utils.data import DataLoader

from arg_parse.AE_args import get_args
from data_loader.AE_dataloader import *
from models.Multi_DAE import *
from models.Multi_VAE import *
from utils.Multi_AE_utils import *
from random import *


@ logging_time
def get_model(args: object, item_encoder: dict):
    model = MultiDAE(
        p_dims=args.p_dims + [len(item_encoder)],
        dropout_rate=args.dropout_rate,
    ).to(args.device)
    
    PATH = args.model_path
    model.load_state_dict(torch.load(PATH))
    
    return model

def main(args: object):
    args.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.randn(4).to(args.device) #  If you pass a dummy input to GPU like torch.randn(4).to(device) then after that you will normal transfer speed.
    dummy_data, item_encoder, item_decoder, house_encoder, house_decoder = \
        get_inference_data(args, generate_encoder_decoder)
    
    model = get_model(args, item_decoder)
    
    inference_result = inference(args, model, dummy_data, item_decoder)
    print(f"Recommended items: {inference_result}")

if __name__ == "__main__":
    args = get_args()
    main(args)