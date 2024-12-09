function main() {
    const nameSlide = 0;
    const templateSlideIndex = 1;

    const presentation = SlidesApp.getActivePresentation();
    const templateSlide = presentation.getSlides()[templateSlideIndex];

    const nameSlideElement = presentation.getSlides()[nameSlide];
    const nameShape = nameSlideElement.getShapes()
        .find(shape => shape.getText().asString()
            .startsWith('Names'));

    if (!nameShape) {
        throw new Error('Name shape not found');
    }

    const names = nameShape.getText().asString()
        .split('\n')
        .slice(1) 
        .map(name => name.trim())
        .filter(name => name.length > 0);

    names.forEach(name => {
        const newSlide = presentation.appendSlide(templateSlide);

        newSlide.getShapes().forEach(shape => {
            if (shape.getText().asString().includes('{{name}}')) {
                shape.getText().setText(shape.getText().asString().replace('{{name}}', name));
            }
        });
    });

    console.log(names);
}

function clearGeneratedSlides() {
    const presentation = SlidesApp.getActivePresentation();
    const slides = presentation.getSlides();

    for (let i = slides.length - 1; i >= 2; i--) {
        slides[i].remove();
    }
}

function onOpen() {
    const ui = SlidesApp.getUi();
    ui.createMenu('Certificate Generator')
        .addItem('Generate Certificates', 'main')
        .addItem('Clear Generated Slides', 'clearGeneratedSlides')
        .addToUi();
}
