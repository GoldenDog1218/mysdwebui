import modules.scripts as scripts
import gradio as gr
#import os

from modules.processing import process_images, Processed
#from modules.shared import opts

# not yet

#BASE_STEPS=40
#BASE_SCALE=10

ResultType = {
    "Not set":"", 
    "摄影":", ((photograph)), highly detailed, sharp focus, 8k, 4k", 
    "数字艺术":", ((digital art)), (digital illustration), 4k, trending on artstation, trending on cgsociety, cinematic, agfacolor", 
    "绘画":", ((painting, canvas, fine art)), detailed", 
    "草图":", ((sketch, drawing)), pencil art, graphite, colored pencil, charcoal art, high contrast, 2 bit", 
    "经典漫画":", ((storybook drawing, graphic novel, comic book)), Jack Kirby, Frank Miller, Steve Ditko, John Romita, Neal Adams", 
    "现代漫画":", ((comic book)), Jim Lee, john romita jr, Cory Walker, ryan ottley",
    "漫画":", ((manga,anime)), Katsuhiro Otomo, Naoki Urasawa, Hiroya Oku, Hiromu Arakawa, Junji Ito,danbooru, zerochan art, kyoto animation"
}

ResultTypeNegatives = {
    "Not set":"", 
    "摄影":", blurry, art, painting, rendering, drawing, sketch", 
    "数字艺术":", blurry, rendering, photography, painting, signature", 
    "绘画":", photography, rendering, signature, wall", 
    "草图":", photography, rendering, painting, signature, text, margin", 
    "经典漫画":", ((logo)), (title), text, speech bubbles, panels, signature, ((barcode)), margin, sticker", 
    "现代漫画":", ((logo)), (title), text, speech bubbles, panels, signature, ((barcode)), margin, sticker", 
    "漫画":", ((logo)), (title), text, panels, speech bubbles, signature, ((barcode)), margin, sticker" 
}

ResultStyle = {
    "Not set":"", 
    "现实主义":", ((realistic)),(realism)", 
    "写实主义":", ((photorealism)),detailed", 
    "超现实主义":", (hyperrealism),(micro details)", 
    "超现实主义2":", (surrealism)", 
    "现代艺术":", (modern art)", 
    "绘画风":", (painterly)", 
    "抽象的":", (abstract art), ", 
    "流行艺术":", (pop art)", 
    "印象派":", (impressionist art)", 
    "立体主义":", (cubism)", 
    "幻想":", (fantasy art)"
}

ResultColors = {
    "Not set":"", 
    "暖色":", warm", 
    "冷色":", cool", 
    "丰富色彩":", colorful", 
    "饱和的":", saturated", 
    "低饱和度":", low coloration", 
    "去饱和":", desaturated", 
    "灰度":", grayscale", 
    "黑与白":", black and white", 
    "互补":", complementary-colors", 
    "非互补":", non-complementary colors", 
    "混乱的":"chaotic colors", 
    "HDR":"HDR", 
    "光":"light"
}

ImageView = {
    "Not set":"", 
    "鱼眼镜头":", fisheye, 10mm, zoomed out, F/22.0, very far away, sharp", 
    "超广角":", super wide angle, 20mm, zoomed out, F/11.0, far away, sharp", 
    "广角":", wide angle, 25mm, 35mm, zoomed out, F/5.6, medium distance, sharp", 
    "人像镜头":", portrait, 50mm, F/2.8, 1m away", 
    "长焦镜头":", telephoto, 100mm, F/5.6, far away, sharp", 
    "超长焦":", super telephoto, F/11.0, 200mm, 300mm, very far away, sharp", 
    "微距镜头":", macro, extremely close, extremely detailed",
    "特写":"(close up),worms-eye view",
    "鸟瞰图":"(birds-eye view),distant"
}

ImageStyle = {
    "No focus":"", 
    "肖像":"", 
    "优雅的画":", Norman Rockwell, Franz Xaver Winterhalter, Jeremy Mann, Artgerm, Ilya Kuvshinov, Anges Cecile, Michael Garmash",
    "怪物":", monster, ugly, surgery, evisceration, morbid, cut, open, rotten, mutilated, deformed, disfigured, malformed, missing limbs, extra limbs, bloody, slimy, goo, Richard Estes, Audrey Flack, Ralph Goings, Robert Bechtle, Tomasz Alen Kopera, H.R.Giger, Joel Boucquemont, artstation",
    "景观":""
}

ImageStyleNegatives = {
    "No focus":"", 
    "肖像":", ((ugly)), ((duplicate)), (morbid), ((mutilated)), (mutated), (deformed), (disfigured), (extra limbs), (malformed limbs), (missing arms), (missing legs), (extra arms), (extra legs), (fused fingers), (too many fingers), long neck, low quality, worst quality", 
    "优雅的画":", ((ugly)), (mutilated), (bad anatomy), (bad proportions), bad hands, text, error, missing fingers, extra digit, cropped, low quality, worst quality",
    "怪物":"(attractive),pretty,smooth,cartoon,pixar,human",
    "景观":", low quality, noise, lowres"
}

class Script(scripts.Script):

    def title(self):
        return "风格控制台"

    def ui(self, is_img2img):

        with gr.Blocks(css=".gradio-container {background-color: red}"):

            with gr.Row():
                poResultType = gr.Radio(list(ResultType.keys()), label="图片类型", value="Not set")
                poResultStyle = gr.Radio(list(ResultStyle.keys()), label="视觉风格", value="Not set")
                poResultColors = gr.Radio(list(ResultColors.keys()), label="色彩", value="Not set")
                poImageView = gr.Radio(list(ImageView.keys()), label="镜头和h视觉", value="Not set")
                
            with gr.Row():
                poImageStyle = gr.Radio(list(ImageStyle.keys()), label="专注于（添加额外提示以改善结果）", value="No focus")
            
            #with gr.Row():
            #    TextToShow = gr.Text(value=poResultType, label="Extra keywords", visible=True, placeholder="Selected keywords will appear here")

        return [poResultType, poResultStyle, poResultColors, poImageView, poImageStyle]

    def run(self, p, poResultType, poResultStyle, poResultColors, poImageView, poImageStyle):
        p.do_not_save_grid = True
        # Add the prompt from above
        p.prompt += ResultType[poResultType] + ResultStyle[poResultStyle] + ResultColors[poResultColors] + ImageView[poImageView] + ImageStyle[poImageStyle]
        p.negative_prompt += ResultTypeNegatives[poResultType] + ImageStyleNegatives[poImageStyle]
      
#        p.cfg_scale=BASE_SCALE
#        p.steps = BASE_STEPS

        proc = process_images(p)
        return proc