
#Load a preset palette, or resort to black/white plot texts/backgrounds
loadPalette = function(defaultBackground = c('#FFFFFF')){
    
    defTheme = c('panelBackground', 'axisBackground', 'textColor')
        hex = c(defaultBackground, defaultBackground, '#000000')
        defPalette = as.list(hex)
        names(defPalette) = defTheme
        return(defPalette)
    
}