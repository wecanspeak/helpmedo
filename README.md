[![Build Status](https://travis-ci.org/wecanspeak/helpmedo.svg?branch=master)](https://travis-ci.org/wecanspeak/helpmedo)

# helpmedo

A secretary you train.

# Usage 
```
$ ./helpmedo.py [-hl] project job [action [sth]]
```

Give it a try.
```
$ ./helpmedo.py demo do_job1
```

A step further.
```
$ ./helpmedo.py demo do_job2 echo "hello world"
```

On Windows platform, please apply
```
$ python helpmedo.py [-hl] project job [action [sth]]
```

# Prerequisites

* [zope interface](https://pypi.org/project/zope.interface/)
* [PyYAML](https://pypi.org/project/PyYAML/)
* [python colorama](https://pypi.org/project/colorama/)

# How to add a new job

Job declaration is integrated in source tree with structure : 

```
job/
  <project>/
    <job>.py
    <job>.yml
```

Create `<job>.py` and `<job>.yml` for a new job within existed or new-added `project` folder.<br>
`<job>.py` implements job details and `<job>.yml` describes job scenario.<br>
To follow straight forward usage, `<project>` is a noun and `<job>` is often a verb.

Please refer to [job/demo](job/demo).

# Unit test

Run `pytest` then check test result.
```
$ pytest
```

# ToDo

* refactor utils folder for versatile types
* todo jobs
  * demo job for creating default job 
  * ssh/rs232 demo example
