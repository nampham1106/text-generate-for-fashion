# text-generate-for-fashion
  Discription: The project focuses on supporting the creation of fashion content.

## Download repository
    git clone https://github.com/nampham1106/text-generate-for-fashion.git

## Download pretrained model
  Download file `model.safetensors` in `train_article/best_model`\
  Link download: https://j2c.cc/models \
  Move file `model.safetensors` into `fastapi/models/`
  
## Build 
    docker-compose build
## Run 
    docker-compose run
  Access the network URL: http://172.27.0.3:8501

  Interface:
  ![image](https://github.com/nampham1106/text-generate-for-fashion/assets/82878964/343e9328-fc85-4da3-8c3b-174e6d3e8977)
  
## Shutdown
    docker-compose down


