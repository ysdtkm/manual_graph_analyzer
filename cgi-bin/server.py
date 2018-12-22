#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi
import cgitb
import datetime
from hashlib import md5
import os
import pickle
import shutil
from string import Template
import sys
from classes import State, Node

def encode(ustr):
    hash = md5(ustr.encode("utf8")).hexdigest()
    return hash

def get_template():
    template = Template("""
        <html>
        <body>
        ${body}
        </body>
        </html>
        """)
    return template

def dump_fieldstorage(fo):
    for k in fo.keys():
        sys.stderr.write(f"Field: {k}, Value: {fo[k].value}\n")

def main_process(fo):
    fname = "state.pkl"
    dump_fieldstorage(fo)
    if os.path.isfile(fname):
        with open(fname, "rb") as f:
            st = pickle.load(f)
    else:
        st = State()
    st = edit_state(st, fo)
    bd = get_main_body(st)
    with open("tmp.pkl", "wb") as f:
        pickle.dump(st, f)
    shutil.move("tmp.pkl", fname)
    return bd

def console(obj):
    sys.stderr.write(str(obj) + "\n")

def edit_state(st, fo):
    if "Add" in fo and "child" in fo:
        console("Add")
        cname = fo["child"].value
        if st.name_exists(cname):
            cid = st.id_by_name(cname)
        else:
            cid = generate_time_hash()
        pids = set()
        if "parent" in fo:
            na = fo["parent"].value
            if st.name_exists(na):
                pids = {st.id_by_name(na)}
        st.enqueue(Node(cid, cname, pids))
    elif "Next" in fo and st.non_empty_queue():
        console("Next")
        st.pop()
    elif "Clear" in fo and "option" in fo and fo["option"].value == "clear":
        console("Clear")
        st = State()
    elif "Rename" in fo and "edited" in fo and "To" in fo:
        console("Rename")
        if st.name_exists(fo["To"].value):
            return st
        if st.name_exists(fo["edited"].value):
            nid = st.id_by_name(fo["edited"].value)
            st.nodes[nid].name = fo["To"].value
    elif "Merge" in fo and "edited" in fo and "Mto" in fo:
        if st.name_exists(fo["edited"].value) and st.name_exists(fo["Mto"].value):
            st.merge_names(fo["edited"].value, fo["Mto"].value)
    elif "Delete" in fo and "edited" in fo:
        console("Delete")
        edited = fo["edited"].value
        if st.name_exists(edited):
            did = st.id_by_name(edited)
            st.delete_by_id(did)
    return st

def get_main_body(st):
    states = str(st)
    st.save_graph()
    rd = datetime.datetime.now().strftime("%H%M%S%f")
    if st.non_empty_queue():
        pid = st.pop(noremove=True)
        p = st.nodes[pid].name
    else:
        p = ""
    bo = f"""
    <h1>Semi-manual graph analyzer (with breadth-first prompt)</h1>
    <h3>Current state</h3>
    <img src="../graph.png?dummy={rd}">
    <br/>

    <h3>Add node/edge</h3>
    <form action="server.py" method="post">
    Parent name (optional): <input type="text" name="parent" value="{p}"><br/>
    Name: <input type="text" name="child" value="" autofocus><br/>
    <input type="submit" value="Add" name="Add">
    <input type="submit" value="Next in queue" name="Next"><br/>
    </form>
    <br/>

    <h3>Edit</h3>
    <form action="server.py" method="post">
    Original name: <input type="text" name="edited" value=""><br/>
    ↓<br/>
    <input type="submit" value="Rename to" name="Rename"><input type="text" name="To" value="">
    <br/>
    <input type="submit" value="Merge to" name="Merge"><input type="text" name="Mto" value="">
    <br/>
    <input type="submit" value="Delete" name="Delete">
    </form>
    <form action="server.py" method="post">
    <input type="submit" value="All clear" name="Clear">
    <input type="text" name="option" value="Type 'clear' to confirm" onfocus='this.value=""'>
    </form>
    <br/>

    <h3>Debug info</h3>
    Queue:<br>
    {st.html_queue()}<br>
    <br>
    Nodes:<br>
    {st.html_nodes()}
    """
    return bo

def generate_time_hash():
    rd = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    hash = md5(rd.encode("utf8")).hexdigest()
    return hash

def main():
    cgitb.enable()
    fo = cgi.FieldStorage()
    msg = main_process(fo)
    print("Content-Type: text/html;charset=utf-8")
    print("")
    di = {"body": msg}
    print(get_template().substitute(di))

if __name__ == "__main__":
    main()
