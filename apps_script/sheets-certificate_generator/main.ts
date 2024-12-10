/// <reference types="google-apps-script" />

function main() {

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    const slideUrl = getTemplateSlidesUrl();
    const presentation = SlidesApp.openByUrl(slideUrl);

    const templateData = getData();

    const templateSlide = presentation.getSlides()[0];
    const templateFields = templateData[0];

    const templateTexBoxes = templateSlide.getShapes()
        .filter(shape => shape.getShapeType() === SlidesApp.ShapeType.TEXT_BOX);

    for (const field of templateFields) {
        if (!templateTexBoxes.some(textBox => textBox.getText().asString().includes(`{{${field}}}`))) {
            throw new Error(`Field '${field}' not found in template slide`);
        }
    };

    for (const data of templateData.slice(1)) {
        const newSlide = presentation.appendSlide(templateSlide);
        const newSlideTextBoxes = newSlide.getShapes()
            .filter(shape => shape.getShapeType() === SlidesApp.ShapeType.TEXT_BOX);

        for (const textBox of newSlideTextBoxes) {
            let text = textBox.getText().asString();
            templateFields.forEach((field, i) => {
                text = text.replace(`{{${field}}}`, data[i]);
            });
            textBox.getText().setText(text);
        };
    }
}


function onOpen() {
    const ui = SpreadsheetApp.getUi();
    ui.createMenu('Certificate Generator')
        .addItem('Generate Certificates', 'main')
        .addItem('Clear Generated Slides', 'clearGeneratedSlides')
        .addToUi();
}

function getTemplateSlidesUrl(): string {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const url = sheet.getRange('B1').getValue();
    if (!url) {
        throw new Error('Template slides url not found. It must be in cell B1');
    }
    return url;
}

function getData(): string[][] {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = sheet.getDataRange().getValues().slice(2);
    return data;
}

function clearGeneratedSlides() {
    const slideUrl = getTemplateSlidesUrl();
    const presentation = SlidesApp.openByUrl(slideUrl);
    const slides = presentation.getSlides();

    for (const slide of slides.slice(1)) {
        slide.remove();
    }
}

export {}; // Prevents "Duplicate function implementation" error
