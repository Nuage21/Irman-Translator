# Irman-Translator

Irman-Translator is a *Rule* & *Statistics* based translation Web app, mainly written in `Django`, `Python` for backend, and uses `Vue.js`, `jQuery` and `Bootstrap` for the front.

It translates between English and [Tamaziɣt](https://en.wikipedia.org/wiki/Berber_languages "Learn about Berber languages")

# Table of Contents

1. [How it works](#how-it-works)
1. [Explaining the algorithm from English to Tamaziɣt](#explaining-the-algorithm-from-english-to-tamazi%C9%A3t)
2. [In Depth](#in-depth)
2. [Contributing](#contributing)
3. [Authors](#authors)

## How it works

Irman-Translator uses both `Human Language Rules` and `Statistics` to provide the most accurate translation, the rules consist of strings so we won't have to touch the code to introduce a new one! These rules contain an if block with a pattern as a condition and a run statement. When applying the rule to a certain phrase, if the pattern fit a part of it, this last will be edited as the rule application says depending of the matched parameters (words). The creator was inspired of Regular Expressions to make this translation system.

## Explaining the Algorithm (From English to Tamaziɣt)

Let's see how Irman-Translator will do its job on the phrases `we're walking` `you're eating` 

The following titles shows the basic steps on which the translator passes through.
## Mapping

It consists of associating each word of the source phrase with its correspondant of the target language;
to do that let's take this dictionary (just for explanation purposes: the mapping algorithm uses `binary search algorithm` over translation data to find the correspondant)

```python
dico = {
  "we're": ['aqlaɣ', 'im'],
  "you're": ['aqlik', 'im'],
  "walking": ['teddu', 'cv'],
  "eating": ['tečč', 'cv']  
}
```
```
cv stands for continuous verb (exemple only)
```
so for exemple we have `we're` that corresponds to `aqlaɣ` which is classified `im` (a unique classifier for `aqli`'s family which is the `to be` in tamaziɣt, also indicates continous form, the name itself does not mean anything, it's only used for rule matching purposes)
  
- When the mapping applied to the two stated above phrases we shoud have something like this `|im|aqlaɣ |cv|teddu` and `|im|aqlik |cv|tečč` respectively.

```
we indicate the word category between two bars to not mix with the word itself chars  
```
### Rules Application

- To create a rule we initiate an instance of the `rule` class with the rule core as constructor parameter.
- To apply it we use the `rule.apply(target_phrase)`.

So let's consider this rule:

```python
rule0 = rule('if(|im|>|0v|):el[0]+ +im_0[0,t-,t-,i-,t-,n-,n-,t-,t-,0,0]'
             '+el[1]+im_0[-eɣ,-ed,-ed,0,0,0,0,-em,-emt,-en,-ent]')

sentence = we're walking, you're eating
mapped_phrase0 = '|im|aqlaɣ |cv|teddu'
mapped_phrase1 = '|im|aqlik |cv|tečč'

translated_phrase0 = rule0.apply(mapped_phrase0)
translated_phrase0 = rule0.apply(mapped_phrase0)

# resituate the sentence (and then the whole translated text with the right separators (commas, dots...))
translated_sentence = translated_phrase0 + ', ' + translated_phrase1 
```
#### In the rule core we have:
- `el[i]` will be replcaed with i'th matched word
- `im_0` means check the `im` corresponding tab to get the index of the 0'th element and replace it with its corresponding in the following tab

When we apply `rule0` to the phrases `mapped_phrase0` and `mapped_phrase1` after mapping the splitted `sentence`, this what happens:

1. iterate over the words (splitted phrase) and check if all with the following it matches the rule pattern & if yes:
  1. el[0] will give `aqlaɣ` and `aqlik` for `mapped_phrase0` and `mapped_phrase1` respectively added to a certain `rslt`
  2. we have `+ +` which means add a space.
  3. then `im_0[0,t-,t-,i-,t-,n-,n-,t-,t-,0,0]`, `apply` will look for the 0'th matched at the `im` corresponding tab, 
     that way:

```python
im_tab = rule.get_corresponding_tab('im') # will return im_tab

# let's consider

im_tab = [
    'aqli',  # for I
    'aqlik',  # for You
    'aqlikem', 
    'atan',  # for He
    'attan', # for She (etc...)
    'aqlaɣ',
    'aqlaɣ',
    'aqlikun',
    'aqlikunt',
    'ahnad',
    'ahnettad',
]
```
  4. The index of aqlaɣ (mapped_phrase0) is 5 for the fifth element of `[0,t-,t-,i-,t-,n-,n-,t-,t-,0,0]` will be replaced 
     with and added to the result, if 0 then we add nothing
  5. We do the same thing for the next elements of the rule application clause
  6. and we get `translated_phrase0 = 'aqlaɣ n-teddu'` and `translated_phrase1 = 'aqlik t-tečč-ed'` and after the 
     restitution `translated_sentence = 'aqlaɣ n-teddu, aqlik t-tečč-ed'`

## In Depth

The exemple above constitutes a little chunk of what the traslator does;

The translator actually apply all the rules he find in `rules.xml` until no rule pattern match is found over the text, remark that when applying a certain rule, another rule pattern can be constructed as a result. And it continues again and again.

The translator also manages language contexts, letters casing, punctuation and much more.

The translation is sent to the user as a response to an `ajax request` when he changes the input text

#### Remarks:
The element and array-by-index replacing is only the basic of the rule application, more features are added as:
- The conditional pattern or display with `?` to make a pattern element as optional (the match is prefered though), or 
  to make something in the application as condictional over a pattern element (ex: `el[0]?2` will be considered only if 
  pattern element 2 was **not conditionally** matched).

- The conditional display with `$` to make something considered only if a certain pattern was **conditionally** matched.

Actually the `rule` applier supports  several features to make creating and editing new rules as easy as possible.

To learn more about the rules creating syntax check  [rule-syntax.pdf](https://github.com/hbFree/Irman-Translator/blob/master/rule-syntax.pdf")



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Consider doing this to set up your developement environment


##Linux
From your terminal:
1. Install **git** if not done yet: `$ sudo apt install git-all`

2. clone the repository:`$ git clone https://github.com/hbFree/Irman-Translator`

3. Enter the project directory: `$ cd Irman-Translator `

4. Run `$ chmod +x linux_setup.sh; ./linux_setup.sh ` to install `python`, `django` and make needed migrations.

##Windows

1. Install `git` if not done yet from [windowd-git install](https://gitforwindows.org/) and `python` from  [python32 for Windows](https://www.python.org/downloads/windows/)

2. clone the repository:`$ git clone https://github.com/hbFree/Irman-Translator`

3. Enter the project directory: `$ cd Irman-Translator `

4. Run `$ win_setup.bat ` to install `python`, `django` and make needed migrations.

---

If you are working on the code then it would be easier if you set up a python test project that contains the code you're working on, by that ou won't have to restart the server.

Finally to test the whole project then you got to start the localhost server: `$ python manage.py runserver`, then  go to your browser and enter to: `http://127.0.0.1:8000/translator` 
## Authors
This project was designed and developed by @hbFree with the help of @kadaitm
> by this shall a language never die!