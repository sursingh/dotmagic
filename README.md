
# Graphviz magic

Simple magic functions that adds support for dropping shadows in diagram

## Install

pip install git+https://github.com/sursingh/dotmagic.git

## Usage

```
%%dot -psK <layout>
 -p: convert image to png (default SVG)
 -s: drop shadows
 -K <layout>: Select the layout
    dot(default), neato, twopi, circle, fdpm sfdp

%dotstr -psK <layout> <dotstr>

```

Also it will expand the local variables

### Simple graph


```python
# Load the magic
%load_ext dotmagic

style='filled'
color='lightblue'
```


```python
%%dot -p
digraph {
    node [color="${color}" style="${style}"]
    a -> {b c}
}
```


![png](README_files/README_3_0.png)



```python
g = '''digraph {
   node [color="${color}" style="${style}"]
    a -> {b c} 
}'''
%dotstr -p g
```


![png](README_files/README_4_0.png)


### Adding a shadow


```python
%%dot -sp
digraph {
    node [color="${color}" style="${style}"]
    a -> {b c}
}
```


![png](README_files/README_6_0.png)


### Change the layout


```python
%%dot -spK neato
digraph {
    node [color="${color}" style="${style}"]
    a -> {b c}
}
```


![png](README_files/README_8_0.png)

