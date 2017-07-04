Script should do follow things:

1. Create 50 zip archives. Each of them should contains 100 xml files
   with random values in follow structure:

.. code-block:: xml

    <root>
    <var name='id' value='<uniq string value>'/>
    <var name='level' value='<random number from range 1 - 100>'/>
    <objects>
    <object name='<random sring value>'/>
    <object name='<random string value>'/>
    …
    </objects>
    </root>


Inside of the tag <objects> random number (from 1 to 10) nested tags of <object>.

2. Process created zip files from step 1.

* Parse xml files
* create 2 csv files with following content:

 - First: id, level - one string for each xml file
 - Second: id, object_name - separate string for each tag <object>, i.e.
   (from 1 to 10 strings for each xml file)

Extra note: Step 2, should fully use resources of multi core processor.

Will be good, if program work fast.
