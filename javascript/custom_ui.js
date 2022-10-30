const defaultPreset = {
  name: '[naifu]',
  prompt: 'masterpiece,best quality, ',
  negative: 'nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry ',
  step: 28,
  method: 'Euler a',
  width: 512,
  height: 768,
  scale: 1.0
}

const defaultPreset512x512 = {
  name: '[naifu-512x512]',
  prompt: 'masterpiece,best quality, ',
  negative: 'nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry ',
  step: 28,
  method: 'Euler a',
  width: 512,
  height: 512,
  scale: 1.0
}

const defaultPreset768x512 = {
  name: '[naifu-768x512]',
  prompt: 'masterpiece,best quality, ',
  negative: 'nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry ',
  step: 28,
  method: 'Euler a',
  width: 768,
  height: 512,
  scale: 1.0
}

const clearPreset = {
  name: '[清除]',
  prompt: '',
  negative: '',
  step: 28,
  method: 'Euler',
  width: 512,
  height: 768,
  scale: 12.0
}

const presetList = [
  clearPreset,
  defaultPreset,
  defaultPreset768x512,
  defaultPreset512x512,
  {name:'作者bilibili'}
]

function querySelector(...args) {
  return gradioApp()?.querySelector(...args)
}

function querySelectorAll(...args) {
  return gradioApp()?.querySelectorAll(...args)
}

function reload_ui() {
  querySelector('#tab_settings #settings ~ div > .gr-button-primary')?.click()
}

function add_custom_ui() {
  if (!document.getElementsByTagName('gradio-app').length) {
    requestAnimationFrame(add_custom_ui)
    return
  }

  if (querySelector('#custom_preset')) return

  const $quicksettingsEl = querySelector('#tab_txt2img')
  if (!$quicksettingsEl) {
    requestAnimationFrame(add_custom_ui)
    return
  }

  const customEl = document.createElement('fieldset')
  customEl.id = 'custom_preset'
  customEl.className = 'flex flex-wrap w-full p-2 my-2 gap-2 border-solid border border-gray-300 rounded-sm text-sm'

  const colorList = ['red', 'blue', 'green', 'orange']

  customEl.innerHTML = `
    <legend class="text-xs text-gray-500">预置</legend>
    ${presetList.map((item, index) => {

    const color = colorList[index % colorList.length]
    const el = `<button class="text-${color}-500" data-name="${item.name}" data-color="${color}">${item.name}</button>`

    return el
  }).join('')}`

  function changeVal(selector, value) {
    const el = querySelector(selector)
    el.value = value

    const event = new Event('input')
    Object.defineProperty(event, 'target', { writable: false, value: el });
    el.dispatchEvent(event)
  }

  customEl.addEventListener('click', (e) => {
    const { target } = e
    const { dataset } = target
    	
    if(dataset.name === '作者bilibili')
    {
    	window.open("https://space.bilibili.com/278946237",'_blank')
    	return
    }

    if (dataset.name) {
      const preset = presetList.find(item => item.name === dataset.name)

      const {
        name,
        prompt,
        negative,
        step,
        method,
        width, height,
        scale
      } = Object.assign({}, defaultPreset, preset)

      console.log('使用预置参数 %s', name, preset);

      const prevActiveEl = target.parentNode.querySelector('button.active')
      if (prevActiveEl) {
        const { color } = prevActiveEl.dataset
        prevActiveEl.className = `text-${color}-500`
      }
      target.className = 'active text-base text-white bg-blue-400 px-1 rounded-sm'

      changeVal('#txt2img_prompt textarea', prompt)
      changeVal('#txt2img_neg_prompt > label > textarea', negative)
      changeVal('#range_id_0', step)
      querySelector(`#txt2img_sampling input[name="radio-txt2img_sampling"][value="${method}"]`)?.click()
      changeVal('#range_id_1', width)
      changeVal('#range_id_2', height)
      changeVal('#range_id_6', scale)
    }
  })

  $quicksettingsEl.insertAdjacentElement('afterbegin', customEl)

  console.log('预置参数面板添加成功, 当前参数列表', presetList)

  const $footer = querySelector('footer')
  $footer.classList.add('items-center')
  const counter = document.createElement('img')
  $footer.insertAdjacentElement('beforeend', counter)
  counter.style = 'height: 44px; margin-left: 4px;'
  counter.src = 'https://count.getloli.com/get/@' + location.host
}

add_custom_ui()
