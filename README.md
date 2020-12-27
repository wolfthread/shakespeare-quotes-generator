# Shakespeare Quotes Generator

Script used to generate the quotes that are fetched from my [Shakespeare Quotes App](https://shakespeare-quotes-gen.herokuapp.com/), of which you can find the [code here](https://github.com/wolfthread/shakespeare-quotes-app).

## Generation of quotes

The file named `themes.txt` contains all the themes to do the search within the Bard's Work. This can be edited, for now manually, and then the python script uses the themes to pull out the quotes accordingy.

The desired end format of the quote is:

> Could such inordinate and low desires, such poor, such bare, such lewd, such mean attempts, such barren pleasures, rude society as thou art matched withal, and grafted to, accompany the greatness of thy blood, and hold their level with thy princely heart?
>
> _(Henry IV, Part I, Act 3, Scene 2)_

Upon runtime, the python code sorts through all the work, splitting each play into scenes and uniting complete sentences within in each scene.

## Source

The initial texts used for this came from [Folger Digital Texts](https://shakespeare.folger.edu/download-the-folger-shakespeare-complete-set/), from [The Folger Shakespeare](<(https://shakespeare.folger.edu/)>), licensed under a [Creative Commons Attribution-NonCommercial 3.0 Unported license](https://creativecommons.org/licenses/by-nc/3.0/deed.en_US).

## License

MIT &copy; 2020, Sylvain Dessureault
