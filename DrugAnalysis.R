# Analysis of trimmed FDA-approved drug list (Original submissions and marketed/OTC)
#
#   Questions:
#       - What is the breakdown of the number of active ingredients in an approved compound?
#       - What is the breakdown of combination clinical trials? 

library(readr, quietly = TRUE)
library(dplyr, quietly = TRUE)
library(ggplot2, quietly = TRUE)
library(RColorBrewer, quietly = TRUE)
library(jsonlite, quietly = TRUE)
library(cowplot, quietly = TRUE)
library(extrafont, quietly = TRUE)
source('src/setup_DrugAnalysis.R')
themePalette = loadPalette()

yearCutoff = 1980

drugDF = as.data.frame(read_csv('ref/ApprovedFDADrugs.csv')) 
drugDF = drugDF[drugDF$Year >= yearCutoff, ]
drugDF = drugDF[(drugDF$Entity == 'NDA' | drugDF$Entity == 'BLA'), ] #Remove generics
drugDF = drugDF %>% select(c('DrugName', 'ActiveIngredient', 'Year', 'Entity')) %>%
     unique() %>% as.data.frame()

#Count number of active ingredients 
drugDF$nIngredients = 0
drugDF$nIngredientFactor = c('0')
for(row in 1:nrow(drugDF)){
    drugDF$nIngredients[row] = length(strsplit(drugDF$ActiveIngredient[row], ';')[[1]])
    if(drugDF$nIngredients[row] > 3){
        drugDF$nIngredientFactor[row] = '>3'
    } else {drugDF$nIngredientFactor[row] = as.character(drugDF$nIngredients[row])}
} 
drugDF$Year = as.numeric(drugDF$Year)
drugDF$nIngredients = as.numeric(drugDF$nIngredients)
drugDF$nIngredientFactor = as.factor(drugDF$nIngredientFactor)
drugDF$nIngredientFactor = factor(drugDF$nIngredientFactor, levels = c('1', '2', '3', '>3'))

shiftGreens = brewer.pal(n = 9, "Greens")[c(4, 5, 7, 9)]

drugPlot = ggplot(drugDF, aes(x = Year, group = nIngredientFactor, fill = nIngredientFactor))+
        geom_bar()+
        theme_light() +
        ggtitle(paste0('FDA-approved drugs & biologics: ', yearCutoff,'-present'))+
        xlab('')+
        ylab(NULL)+
        scale_y_continuous(limits = c(0, 150), expand = c(0, 0))+
        scale_fill_manual(values = shiftGreens)+
        theme(axis.text.x = element_text(size = 14, family = themePalette[['Uniform']]), 
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank(),
            axis.title = element_text(size = 12, face = "bold", family = themePalette[['Uniform Black']]), 
            legend.title = element_text(size = 15, face = "bold", family = themePalette[['Uniform Black']]), 
            legend.text = element_text(size = 15, family = themePalette[['Uniform']]),
            legend.margin = margin(5, 45, 5, 0), 
            legend.key.size = unit(0.5, 'cm'),
            title = element_text(size = 14, face = "bold", family = themePalette[['Uniform Black']]), 
            panel.grid = element_blank(),
            plot.title = element_text(hjust = 0.5),
            panel.background = element_rect(fill = themePalette[['panelBackground']])) + 
        guides(fill = guide_legend(title = "Active\ncompounds"))

drugPlotCap = drugPlot + labs(caption = 'Data source: Drugs@FDA') + 
    theme(plot.caption = element_text(size = 14, color = 'grey50', hjust = 0,
    face = 'plain', margin = margin(t = -2, b = 7.5)))

clinTrials = fromJSON(txt = readLines('ClinicalTrialQuery.json'))
comboDF = NULL
for(trial in names(clinTrials)){
    year = clinTrials[[trial]]$Year
    combo = clinTrials[[trial]]$Combination 
    comboDF = rbind(comboDF, c(year, combo))
}

comboDF = as.data.frame(comboDF)
colnames(comboDF) = c('Year', 'Combination')
comboDF$Year = as.numeric(comboDF$Year)
comboDF = comboDF[comboDF$Year >= yearCutoff, ]
comboDF$Combination[comboDF$Combination == 0] = 'Single'
comboDF$Combination[comboDF$Combination == 1] = 'Combination'
comboDF$Combination = factor(comboDF$Combination, levels = c('Single', 'Combination'))

trialPlot = ggplot(comboDF, aes(x = Year, group = Combination, fill = Combination))+
        geom_bar()+
        theme_light() +
        ggtitle(paste0('Pharmacological clinical trials: ', min(comboDF$Year), '-present'))+
        xlab(NULL)+
        ylab(NULL)+
        scale_y_continuous(limits = c(0, 6750), expand = c(0, 0))+
        scale_fill_manual(values = c(shiftGreens[1], shiftGreens[3])) +
        theme(axis.text.x = element_text(size = 14, family = themePalette[['Uniform']]),
            axis.text.y = element_blank(),
            axis.ticks.y = element_blank(),
            axis.title = element_text(size = 12, face = "bold", family = themePalette[['Uniform Black']]), 
            legend.title = element_text(size = 15, face = "bold", family = themePalette[['Uniform Black']]), 
            legend.text = element_text(size = 15, family = themePalette[['Uniform']]), 
            legend.margin = margin(5, 15, 5, 2),
            legend.key.size = unit(0.5, 'cm'),
            title = element_text(size = 14, face = "bold", family = themePalette[['Uniform Black']]), 
            panel.grid = element_blank(),
            plot.title = element_text(hjust = 0.5),
            panel.background = element_rect(fill = themePalette[['panelBackground']])) + 
        guides(fill = guide_legend(title = "Treatment"))

trialPlotCap = trialPlot + labs(caption = 'Data source: Clinicaltrials.gov') + 
    theme(plot.caption = element_text(size = 14, color = 'grey50', hjust = 0,
    face = 'plain', margin = margin(t = 10)))

outCowLabCap = plot_grid(drugPlotCap, trialPlotCap, nrow = 2, labels = 'auto', 
    align = 'v', label_size = 14, label_fontfamily = themePalette[['Uniform Black']], hjust = -0.1, 
    vjust = 1.3, rel_heights = c(1, 0.95))

ggplot2::ggsave('plots/DrugsFDACaption.png', plot = drugPlotCap, width = 8, height = 5.5, dpi = 600)
ggplot2::ggsave('plots/ClinTrialsCaption.png', plot = trialPlotCap, width = 8, height = 5.5, dpi = 600)
ggplot2::ggsave('plots/Drug&TrialAnalysisLabelCaption.png', plot = outCowLabCap, width = 9, height = 7.25, dpi = 600)
