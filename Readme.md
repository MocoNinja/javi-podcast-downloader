# Readme

## Setup

* `python -m venv venv`
* Use that, like `.\venv\Scripts\activate`
* `pip install -r .\requirements.txt`


## Tools

isort .
autoflake --in-place --remove-all-unused-imports -r .
black .

## Providers


### Youtube

1. Los vídeos parten de `ytd-rich-grid-renderer`
    1. Al cargar esta content (`/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]`)
    1. Dentro tiene elementos con los vídeos
    1. Cambia según el viewport
    1. Los selectores son del tipo `/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-item-renderer[1]`
    1. Hay varios `ytd-rich-item-renderer` con *mucha* mierda dentro a parte de la info del vídeo
1. Al hacer scroll, se añaden más de esos
1. He visto que el último elemento
   1. Es `ytd-continuation-item-renderer`
   1. Tiene selector `/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-continuation-item-renderer`
   1. Cuando haces el scroll para triggear un load de data, se borra y se meten ahi los nuevos elementos, apareciendo uno nuevo al final
   2. Si borras desde las herramientas los elementos, se autocargan
   

#### IDEA SCRAPPING

1. Coger el ytd-rich-grid-renderer
2. Coger los ytd-rich-item-renderer y contarlos
3. Hacer el scroll
4. Coger los ytd-rich-item-renderer NUEVO (usando el indice)