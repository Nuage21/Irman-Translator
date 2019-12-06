# Irman-Translator

Irman-Translator is a *Rule* & *Statistics* based translation Web app, mainly written in **Django Python** for backend, and uses **Vue.js**, **jQuery** and **Bootstrap** for the front.

It translates between English and [Tamaziɣt](https://en.wikipedia.org/wiki/Berber_languages "Learn about Berber languages")

# Table of Contents

1. [How it works](#how-it-works)
1. [Explaining the algorithm from English to Tamaziɣt](#explaining-the-algorithm-from-english-to-tamazi%C9%A3t)
2. [Remarks](#remarks)
2. [Contributing](#contributing)
3. [Authors](#authors)

## How it works

Irman-Translator uses both `Human Language Rules` and `Statistics` to provide the most accurate translation, the rules consist of strings so we won't have to touch the code to introduce a new one! These rules contain an if block with a pattern as a condition and a run statement. When applying the rule to a certain phrase, if the pattern fit a part of it, this last will be edited as the rule application says depending of the matched parameters (words). The creator was inspired of Regular Expressions to make this translation system.

## Explaining the Algorithm (From English to Tamaziɣt)

Let's see how Irman-Translator will do its job on the phrases `we're walking` `you're eating` 

### Mapping (Step-0)

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
### Applying Rules (Step-1)

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

#### Remarks
The element and array-by-index replacing is only the basic of the rule application, more features are added as:
- The conditional pattern or display with `?` to make a pattern element as optional (the match is prefered though), or 
  to make something in the application as condictional over a pattern element (ex: `el[0]?2` will be considered only if 
  pattern element 2 was **not conditionally** matched)
- The conditional display with $ to make something considered only if a certain pattern was **conditionally**  
### Repeat applying rules until no match found (step-2)
### Remove the left category indicators from the beginings of words as `|cv|coding` (step-3)
### The translation is sent as a response to an `ajax request` from the user

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors
This project was designed and developed by @hbFree with the help of @kadaitm
> by this shall a language never die!