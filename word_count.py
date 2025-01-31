function wordCount(text) {
    const words = text.toLowerCase().split(" ");
    const wordMap = {};
    words.forEach(word => {
        if (word in wordMap) {
            wordMap[word] += 1;
        } else {
            wordMap[word] = 1;
        }
    });
    return wordMap;
}
const text = "Hello world! Hello AI. Hello AI world!";
console.log(wordCount(text))
