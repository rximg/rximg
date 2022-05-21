from click import style
import cv2
from numpy import ndarray


import os
import sys
sys.path.append('.')
import os.path as osp
try:
    import paddlehub as hub
    from engine.decorator import ExeStack, rx_func

except Exception as e:
    from engine.decorator import fake_rx_func as rx_func


def cached_model(func_uniquekey,model_type,*args,**kwargs):
    if func_uniquekey not in ExeStack.model_register.keys():

        model = hub.Module(name=model_type,*args,**kwargs)
    else:
        model = ExeStack.model_register[func_uniquekey]
    return model

@rx_func()
def result_img_show(input_):
    if isinstance(input_,list):
        input_ = input_[0]
    if isinstance(input_,ndarray):
        return input_
    elif isinstance(input_,dict):
        if 'save_path' in input_.keys():
        
            return cv2.imread(input_['save_path'])
    return input_

@rx_func()
def run_pbhub_classification(
    image,
    use_gpu:bool=False,
    top_k:int=1,
    model_type:str = "mobilenet_v3_small_imagenet_ssld",
    func_uniquekey:str = "classification",
):
    print('model type',model_type)
    return cached_model(
        func_uniquekey,
        model_type,
        ).classification(
            images=[image],
            use_gpu=use_gpu,
            top_k=top_k
        )



@rx_func()
def run_pdhub_object_detection(
    image:ndarray,
    use_gpu:bool=False,
    score_thresh:float=0.5,
    output_dir:str='resultimg',
    model_type:str = "yolov3_mobilenet_v1_coco2017",
    func_uniquekey:str = "object_detection",
):
    return cached_model(
        func_uniquekey,
        model_type
    ).object_detection(
        images=[image,],
        use_gpu=use_gpu,
        score_thresh=score_thresh,
        output_dir=output_dir)
    # return result


@rx_func()
def run_pdhub_semantic_segmentation(
    image:ndarray,
    save_path:str='resultimg',
    num_classes:int=2,
    model_type='ocrnet_hrnetw18_voc',
    func_uniquekey:str = "semantic_segmentation"
):
    return cached_model(
        func_uniquekey,
        model_type,
        num_classes=num_classes
    ).predict(
        images=[image],
        save_path=save_path
    )

@rx_func()
def run_pdhub_recognize_text(
    image:ndarray,
    use_gpu:bool=False,
    output_dir:str='resultimg',
    box_thresh:float=0.5,
    text_thresh:float=0.5,
    angle_classification_thresh:float=0.9,
    model_type:str='chinese_ocr_db_crnn_mobile',
    func_uniquekey:str = "recognize_text"
):
    return cached_model(
        func_uniquekey,
        model_type
    ).recognize_text(
        images = [image],
        use_gpu=use_gpu,
        output_dir=output_dir,
        visualization=True,
        box_thresh=box_thresh,
        text_thresh=text_thresh,
        angle_classification_thresh=angle_classification_thresh,
    )

    
@rx_func()
def run_pdhub_style_transfer(
    origin:ndarray,
    style:ndarray,
    save_path:str='resultimg',
    model_type:str='msgnet',
    func_uniquekey:str = "style_transfer"
    ):
    return cached_model(
        func_uniquekey,
        model_type
    ).predict(
        [origin],
        style,
        save_path=save_path
    )

if __name__ == '__main__':
    im = cv2.imread(r"C:\Users\kk\Desktop\textcarrc.jpg")
    # results = run_pdhub_recognize_text(
    #     image=im,
    # )
    # results = run_pdhub_semantic_segmentation(
    #     image=im,
    # )
    results = run_pdhub_style_transfer(
        origin=im,
        style=im
    )
    # [{'book jacket': 0.3267041742801666}]
    # [{'data': [], 'save_path': 'resultimg\\image_numpy_0.jpg'}]
    # ndarray
    # ndarray
    print(results)