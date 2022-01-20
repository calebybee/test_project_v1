*****************************************************
Reading PDF Files Through MSAA 
*****************************************************

Microsoft Active Accessibility defines the ``IAccessible`` interface to applications. This interface consists of a set of methods and properties that are defined in the MSAA documentation.

Acrobat implements and exports a set of ``IAccessible`` objects of different types to represent a document, its pages, and other elements of the document hierarchy.

An MSAA client can retrieve an ``IAccessible`` object for a user interface element in the following four ways:

-  Set a ``WinEvent`` hook, receive a notification, and call ``AccessibleObjectFromEvent`` to retrieve an ``IAccessible`` interface pointer for the user interface element that generated the event. See `See Handling event notifications <AccessOverview.html#21082>`__ for details.
-  Call ``AccessibleObjectFromWindow`` and pass the user interface element's window handle. Each open document in Acrobat is associated with its own window handle.
-  Call ``AccessibleObjectFromPoint`` and pass a screen location that lies within the user interface element's bounding rectangle.
-  Call an ``IAccessible`` method such as ``accNavigate`` or ``get_accParent`` to move to a different ``IAccessible`` object.

Acrobat implementation of IAccessible objects
=============================================

Each type of ``IAccessible`` object has a different implementation of the standard methods:

-  form fields are explicitly identified through MSAA.
-  paragraphs, and other elements of document structure are only represented implicitly.

.. note::

   These elements are explicit in the DOM interface; see `See Reading PDF Files Through the DOM Interface <Access_DOM.html#30124>`__.

For each document, Acrobat builds a tree of ``IAccessible`` objects representing the document and its internal structure. Because there is just one window handle associated with the document, Acrobat posts all event notifications to that window. In each notification, a ``childID`` identifies an ``IAccessible`` object for an element in the document. For example, when the user tabs to the next link, the ``EVENT_OBJECT_FOCUS`` notification includes a ``childID`` that is the UID of the link object. See `See Handling event notifications <AccessOverview.html#21082>`__.

The following interfaces are exported from the ``IAccessible`` object by Acrobat:

IGetPDDomNode interface
=======================

This interface exports one function, ``get_PDDomNode`` , which returns a DOM object. The methods described in `See Reading PDF Files Through the DOM Interface <Access_DOM.html#30124>`__" can then be used on this object.

get_PDDomNode
-------------

Returns a DOM object. For more information, see `See Reading PDF Files Through the DOM Interface <Access_DOM.html#30124>`__.

``varID`` is the same as for the other MSAA methods (see `See Descriptive properties and methods <test_with_code.html#89440>`__)

Syntax
~~~~~~

HRESULT get_PDDomNode( VARIANT varID, IPDDomNode **ppDispDoc);

ISelectText interface
=====================

In Acrobat 7.0, the ``ISelectText`` interface is an interface exported by the ``IAccessible`` objects. It exports one function, ``selectText`` , that sets the text selection, but specifies the end location via ``IAccessible`` objects instead of DOM nodes. The ``ISelectText`` interface is available from the root ``IAccessible`` object.

selectText
----------

Sets the text selection. ``startAccID`` and ``endAccID`` are the ``accID`` identifiers for the starting and ending ``IAccessible`` elements, and ``startIndex`` and ``endIndex`` are zero-based indexes into the text of those ``IAccessible`` objects.

.. _syntax-1:

Syntax
~~~~~~

::

   LRESULT selectText(
   long startAccID,
   long startIndex,
   long endAccID,
   long endIndex);

Identifying IAccessible objects in a document
=============================================

You can identify the type of an ``IAccessible`` object by using the ``get_accRole`` method to get its Role attribute. However, you must also distinguish individual objects from others of the same type. You can do this by means of a unique identifier (UID) defined by Acrobat.

The ``IAccessible`` objects defined by Acrobat export a private interface, ``IAccID`` , defined in the file ``IAccID.h`` . It contains one function, ``get_accID`` . Use this UID to determine when two ``IAccessible`` objects refer to the same element in the document.

When a value-change notification or a focus notification has a non-zero ``childID`` , the value of ``childID`` is the UID of one of the objects on the page or document. Use the UID to uniquely identify the object that is the target of the notification.

get_accID
---------

Returns an identifier that is unique within the open document or page.

.. _syntax-2:

Syntax
~~~~~~

HRESULT get_accID(long *id);

Parameters
~~~~~~~~~~

 
 

+----+------------------------------------------------------------------------------------------------------------+
| id | (Filled by the method) Returns the unique identifier of the ``IAccessible`` object. Must not be ``NULL`` . |
+----+------------------------------------------------------------------------------------------------------------+

Returns
~~~~~~~

Always returns ``s_ok`` .

Example
~~~~~~~

IAccID *pID; long uid; /
query for the IAccID interface */ RESULT hr = pObj->QueryInterface (IID_IAccID, reinterpret_cast<void **>(&pID)); if (!FAILED(hr)) { pID->get_accID(&uid); pID->Release(); }

.. note::

   If you obtained the ``IAccessible`` object via a call to ``AccessibleObjectFrom`` *XXX
, it is not possible to query directly for this private interface. In that case, you must use this alternate code:

IServiceProvider *sp = NULL; hr = n->QueryInterface(IID_IServiceProvider, (LPVOID*)&sp); if (SUCCEEDED(hr) && sp) { hr = sp->QueryService(SID_AccID, IID_IAccID, (LPVOID*)&pID); sp->Release(); }

IAccessible method summary
==========================

This section provides a brief syntax summary of the ``IAccessible`` interface methods as defined by MSAA. All methods return ``HRESULT`` . The methods and properties are organized into the following groups:

-  `See Navigation and hierarchy <test_with_code.html#73526>`__
-  `See Descriptive properties and methods <test_with_code.html#89440>`__
-  `See Selection and focus <test_with_code.html#22290>`__
-  `See Spatial mapping <test_with_code.html#57514>`__

Navigation and hierarchy
========================

hierarchy.

accNavigate
-----------

Traverses to another user interface element within a container and retrieves the object. All visual objects support this method.

.. _syntax-3:

Syntax
~~~~~~

accNavigate (long navDir, VARIANT varStart, VARIANT
pvarEnd);

Properties
~~~~~~~~~~

.. _section-1:

 
 

+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *navDir
[in]                     | The direction to navigate, in spatial order or logical order. These are the spatial navigation constants:                                                                                                                                                                                      |
|                                   |                                                                                                                                                                                                                                                                                                |
|                                   | NAVDIR_UP NAVDIR_DOWN NAVDIR_RIGHT NAVDIR_LEFT                                                                                                                                                                                                                                                 |
|                                   | These are the logical navigation constants:                                                                                                                                                                                                                                                    |
|                                   |                                                                                                                                                                                                                                                                                                |
|                                   | NAVDIR_FIRSTCHILD NAVDIR_LASTCHILD NAVDIR_NEXT NAVDIR_PREVIOUS                                                                                                                                                                                                                                 |
|                                   |                                                                                                                                                                                                                                                                                                |
|                                   | -  All ``accNavigate`` methods in PDF objects support the logical navigation directions. Only a few (PDF Structure Element, PDF ComboBox Form Field, and PDF ListBox Form Field) support the spatial navigation directions. Spatial navigation is only supported where it is explicitly noted. |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *varStart
                       | ``CHILDID_SELF`` to start navigation at the object itself, a child ID to start at one of the object's child elements.                                                                                                                                                                          |
|                                   |                                                                                                                                                                                                                                                                                                |
| [in]                              |                                                                                                                                                                                                                                                                                                |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *pvarEnd
                        | Returns a structure that contains information about the destination object. See MSAA documentation for details.                                                                                                                                                                                |
|                                   |                                                                                                                                                                                                                                                                                                |
| [out, retval]                     |                                                                                                                                                                                                                                                                                                |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-1:

Returns
~~~~~~~

``HRESULT``

get_accChild
------------

Retrieves an ``IDispatch`` interface pointer for the specified child, if one exists. All objects support this property.

.. _syntax-4:

Syntax
~~~~~~

get_accChild (VARIANT *varChildID
, IDispatch** *ppdispChild* );

.. _properties-1:

Properties
~~~~~~~~~~

.. _section-2:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| *varChildID
[in]                 | The child ID for which to obtain a pointer. This can be a UID or the 1-based index of the child to retrieve. |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| *ppdispChild
                    | Returns the address of the child's ``IDispatch`` interface.                                                  |
|                                   |                                                                                                              |
| [out, retval]                     |                                                                                                              |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+

.. _returns-2:

Returns
~~~~~~~

``HRESULT``

get_accChildCount
-----------------

Retrieves the number of children that belong to this object. All objects support this property.

.. _syntax-5:

Syntax
~~~~~~

get_accChildCount (long
*pcountChildren* );

.. _properties-2:

Properties
~~~~~~~~~~

.. _section-3:

 
 

+-----------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------+
| *pcountChildren
                 | Returns the number of children. The children are accessible objects or child elements. If the object has no children, this value is zero. |
|                                   |                                                                                                                                           |
| [out, retval]                     |                                                                                                                                           |
+-----------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-3:

Returns
~~~~~~~

``HRESULT``

get_accParent
-------------

Retrieves an ``IDispatch`` interface pointer for the parent of this object. All objects support this property.

.. _syntax-6:

Syntax
~~~~~~

get_accParent (IDispatch*
*ppdispParent* );

.. _properties-3:

Properties
~~~~~~~~~~

.. _section-4:

 
 

+-----------------------------------+--------------------------------------------------------------+
| *ppdispParent
                   | Returns the address of the parent's ``IDispatch`` interface. |
|                                   |                                                              |
| [out, retval]                     |                                                              |
+-----------------------------------+--------------------------------------------------------------+

.. _returns-4:

Returns
~~~~~~~

``HRESULT``

Descriptive properties and methods
==================================

This section provides information on the descriptive APIs.

accDoDefaultAction
------------------

Performs the object's default action. Not all objects have a default action.

.. _syntax-7:

Syntax
~~~~~~

accDoDefaultAction (VARIANT *varID
);

.. _properties-4:

Properties
~~~~~~~~~~

.. _section-5:

 
 

+--------------+----------------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in] | ``CHILDID_SELF`` to perform the action for the object itself, a child ID to perform the action for one of the object's child elements. |
+--------------+----------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-5:

Returns
~~~~~~~

``HRESULT``

get_accDefaultAction
--------------------

default action. Not all objects have a default action.

.. _syntax-8:

Syntax
~~~~~~

get_accDefaultAction(VARIANT *varID
, BSTR* *pszDefaultAction* );

.. _properties-5:

Properties
~~~~~~~~~~

.. _section-6:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *pszDefaultAction
               | Returns a localized string that describes the default action for the object, or ``NULL`` if this object has no default action.   |
|                                   |                                                                                                                                  |
| [out, retval]                     |                                                                                                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

.. _returns-6:

Returns
~~~~~~~

``HRESULT``

get_accDescription
------------------

visual appearance of the object. Not all objects have a description.

.. _syntax-9:

Syntax
~~~~~~

get_accDescription (VARIANT *varID
, BSTR* *pszDescription* );

.. _properties-6:

Properties
~~~~~~~~~~

.. _section-7:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *pszDescription
                 | Returns a localized string that describes the object, or ``NULL`` if this object has no description.                             |
|                                   |                                                                                                                                  |
| [out, retval]                     |                                                                                                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

.. _returns-7:

Returns
~~~~~~~

``HRESULT``

get_accName
-----------

name of the object. All objects have a name.

.. _syntax-10:

Syntax
~~~~~~

get_accName (VARIANT *varID
, BSTR* *pszName* );

.. _properties-7:

Properties
~~~~~~~~~~

.. _section-8:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *pszName
                        | Returns a localized string that contains the name of the object.                                                                 |
|                                   |                                                                                                                                  |
| [out, retval]                     |                                                                                                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

.. _returns-8:

Returns
~~~~~~~

``HRESULT``

get_accRole
-----------

role of the object. All objects have a role.

.. _syntax-11:

Syntax
~~~~~~

get_accRole (VARIANT *varID
, VARIANT* *pvarRole* );

.. _properties-8:

Properties
~~~~~~~~~~

.. _section-9:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *pvarRole
                       | Returns a structure that contain an object role constant in its ``IVal`` member.                                                 |
|                                   |                                                                                                                                  |
| [out, retval]                     |                                                                                                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

.. _returns-9:

Returns
~~~~~~~

``HRESULT``

get_accState
------------

state of the object. All objects have a state.

.. _syntax-12:

Syntax
~~~~~~

get_accState (VARIANT *varID
, VARIANT* *pvarState* );

.. _properties-9:

Properties
~~~~~~~~~~

.. _section-10:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *pvarRole
                       | Returns a structure that contain an object state constant in its ``IVal`` member.                                                |
|                                   |                                                                                                                                  |
| [out, retval]                     |                                                                                                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

.. _returns-10:

Returns
~~~~~~~

``HRESULT``

get_accValue
------------

value of the object. Not all objects have a value.

.. _syntax-13:

Syntax
~~~~~~

get_accValue (VARIANT *varID
, BSTR* *pszValue* );

.. _properties-10:

Properties
~~~~~~~~~~

.. _section-11:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+
| *pszValue
                       | Returns a localized string that contains the current value of the object.                                                        |
|                                   |                                                                                                                                  |
| [out, retval]                     |                                                                                                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------+

.. _returns-11:

Returns
~~~~~~~

``HRESULT``

Selection and focus
===================

This section provides information on the selection and focus APIs.

accSelect
---------

keyboard focus of the object. All objects that support selection or receive the keyboard focus support this method.

.. _syntax-14:

Syntax
~~~~~~

accSelect (long *flagsSelect
, VARIANT *varID* );

.. _properties-11:

Properties
~~~~~~~~~~

.. _section-12:

 
 

+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| *flagsSelect
[in]                | Flags that control how the selection or focus operation is performed. A logical OR of these ``SELFLAG`` constants:        |
|                                   |                                                                                                                           |
|                                   | SELFLAG_NONE SELFLAG_TAKEFOCUS SELFLAG_TAKESELECTION SELFLAG_EXTENDSELECTION SELFLAG_ADDSELECTION SELFLAG_REMOVESELECTION |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]                      | ``CHILDID_SELF`` to select the object itself, a child ID to select one of the object's child elements.                    |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------+

.. _returns-12:

Returns
~~~~~~~

``HRESULT``

get_accFocus
------------

Retrieves the object that has the keyboard focus. All objects that receive the keyboard focus support this property.

.. _syntax-15:

Syntax
~~~~~~

get_accFocus (VARIANT
*pvarID* );

.. _properties-12:

Properties
~~~~~~~~~~

.. _section-13:

 
 

+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| *pvarID
                         | Returns the address of a ``VARIANT`` structure that contains information about the object that has the focus. See MSAA documentation for details. |
|                                   |                                                                                                                                                   |
| [out, retval]                     |                                                                                                                                                   |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-13:

Returns
~~~~~~~

``HRESULT``

get_accSelection
----------------

Retrieves the selected children of the object. All objects that support selection support this property.

.. _syntax-16:

Syntax
~~~~~~

get_accSelection (VARIANT
*pvarChildren* );

.. _properties-13:

Properties
~~~~~~~~~~

.. _section-14:

 
 

+-----------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| *pvarChildren
                   | Returns the address of a ``VARIANT`` structure that contains information about the selected children. See the MSAA documentation for details. |
|                                   |                                                                                                                                               |
| [out, retval]                     |                                                                                                                                               |
+-----------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-14:

Returns
~~~~~~~

``HRESULT``

Spatial mapping
===============

accLocation
-----------

screen location. All visual objects support this method.

.. _syntax-17:

Syntax
~~~~~~

accLocation (long
*pxLeft* , long* *pyTop* , long* *pcxWidth* , long* *pcyHeight* , VARIANT *varID* );

.. _properties-14:

Properties
~~~~~~~~~~

.. _section-15:

 
 

+--------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| *pxLeft, pxTop
[out]    | Return the x and y screen coordinates of the upper-left boundary of the object's location. (The origin is the upper left corner of the screen.) |
+--------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| *pxWidth, pxHeight
[in] | Return the object's width and height in pixels.                                                                                                 |
+--------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| *varID
[in]             | ``CHILDID_SELF`` to get information for the object itself, a child ID to get information for one of the object's child elements.                |
+--------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-15:

Returns
~~~~~~~

``HRESULT``

accHitTest
----------

Retrieves the object at a specific screen location. All visual objects support this method.

.. _syntax-18:

Syntax
~~~~~~

accHitTest (long, long, VARIANT
pvarID);

.. _properties-15:

Properties
~~~~~~~~~~

.. _section-16:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *pxLeft, pxTop
[in]              | The x and y screen coordinates of the point to test. (The origin is the upper left corner of the screen.)                                                                                                                                                                                                                                                                                                    |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| *pvarID
[out, retval]            | Address of a ``VARIANT`` structure that identifies the object at the specified point. The information returned depends on the location of the specified point in relation to the object whose ``accHitTest`` method is being called. You can use this method to determine whether the object at that point is a child of the object for which the method is called. For details, see the MSAA documentation. |
|                                   |                                                                                                                                                                                                                                                                                                                                                                                                              |
|                                   | -  For PDF objects, hit testing has been implemented in a very basic way; it does not identify the boundaries of the object itself with fine granularity, but reports whether or not the tested location is within the bounding box of an element or subtree.                                                                                                                                                |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. _returns-16:

Returns
~~~~~~~

``HRESULT``

IAccessible object types for PDF
================================

This section describes the MSAA ``IAccessible`` object types that are defined to represent PDF documents and their elements. For each object, its methods are listed along with notes on how the implementation is specific to the object type.

.. note::

   Methods that are not listed are not implemented for a given object type.

The objects are:

-  `See PDF Document <test_with_code.html#39396>`__
-  `See PDF Page <test_with_code.html#89992>`__
-  `See PDF Protected Document <test_with_code.html#72837>`__
-  `See Empty PDF Document <test_with_code.html#10863>`__
-  `See PDF Structure Element <test_with_code.html#77828>`__
-  `See PDF Content Element <test_with_code.html#23328>`__
-  `See PDF Comment <test_with_code.html#22500>`__
-  `See PDF Link <test_with_code.html#55866>`__
-  `See PDF Text Form Field <test_with_code.html#40546>`__
-  `See PDF Button Form Field <test_with_code.html#91493>`__
-  `See PDF CheckBox Form Field <test_with_code.html#13511>`__
-  `See PDF RadioButton Form Field <test_with_code.html#19394>`__
-  `See PDF ComboBox Form Field <test_with_code.html#25792>`__
-  `See PDF List Box Form Field <test_with_code.html#20747>`__
-  `See PDF Digital Signature Form Field <test_with_code.html#91488>`__
-  `See PDF Caret <test_with_code.html#49405>`__

The following are some general notes:

-  PDF form fields generally correspond closely to standard user interface elements described in the MSAA SDK document. The ``IAccessible`` objects of form fields attempt to match the behavior described in Appendix A, "Supported User Interface Elements," of the MSAA document. An exception is the PDF combo box, which has a much simpler structure.
-  Form fields, links, and comments, as well as the document as a whole, can take keyboard focus. Subparts of the document (sections, paragraphs, and so on) cannot take focus.
-  A document's contents may be only partially visible on the screen. The ``get_accLocation`` method for a given object returns the screen location of the visible part of the object only. You can use this method to determine which portions of the content are visible.

PDF Document
------------

Represents the contents of an entire PDF document. The subtree of ``IAccessible`` objects beneath the PDF Document object reflects the logical structure of the document.

.. note::

   Content that is not part of the logical structure, such as page headers and footers, is not presented through the MSAA interface.

.. _section-17:

 
 

+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method             | Implementation notes                                                                                                                                                                |
+====================+=====================================================================================================================================================================================+
| accHitTest         | Returns the object at a given location if the location is within the document's bounding box.                                                                                       |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation        | Returns the screen coordinates of the visible part of the document.                                                                                                                 |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate        | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                                                                        |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect          | For ``SELFLAG_TAKEFOCUS`` , the focus is set to the window containing the document and the document is positioned at the beginning. The other ``SELFLAG`` values are not supported. |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChild       | Returns a child object.                                                                                                                                                             |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount  | Returns the number of child objects beneath this one.                                                                                                                               |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDescription | The description contains the full path name of the document and the number of pages it contains: "fileName, XXX pages".                                                          |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus       | Returns the object that has the keyboard focus if it is this object or its child.                                                                                                   |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent      | The parent is ``NULL`` .                                                                                                                                                            |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole        | The role is ``ROLE_SYSTEM_DOCUMENT`` .                                                                                                                                              |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection   | Returns ``NULL`` .                                                                                                                                                                  |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState       | The state is ``STATE_SYSTEM_READONLY`` .                                                                                                                                            |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue       | If the root of the structure tree has an ``Alt`` attribute, the value is the contents of the ``Alt`` attribute.                                                                     |
+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Page
--------

Represents the contents of one page of a PDF document. The subtree of ``IAccessible`` objects beneath the PDF Page node reflects the logical structure of the page.

.. note::

   Content that is not part of the logical structure, such as page headers and footers, is not presented through the MSAA interface.

.. _section-18:

 
 

+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method             | Implementation notes                                                                                                                                                  |
+====================+=======================================================================================================================================================================+
| accHitTest         | Returns the object at the given location if the location is within the page's bounding box.                                                                           |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation        | Returns the screen coordinates of the visible part of the page.                                                                                                       |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate        | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                                                          |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect          | For ``SELFLAG_TAKEFOCUS`` , the focus is set to the window containing the page and the page is positioned at the top. The other ``SELFLAG`` values are not supported. |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChild       | Returns a child object.                                                                                                                                               |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount  | Returns the number of child objects beneath this one.                                                                                                                 |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDescription | The description contains the full path name of the document and the page number of the page: "fileName, page XXX".                                                 |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus       | Returns the object that has the keyboard focus if it is this object or its child.                                                                                     |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent      | The parent is ``NULL`` .                                                                                                                                              |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole        | A custom role, ``Page`` , is defined for this object.                                                                                                                 |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection   | Returns ``NULL`` .                                                                                                                                                    |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState       | The state is ``STATE_SYSTEM_READONLY`` .                                                                                                                              |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue       | If the root of the structure tree has an ``Alt`` attribute, the value is the contents of the ``Alt`` attribute                                                        |
+--------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Protected Document
----------------------

Represents a protected document. When the permissions associated with a document disable accessibility, the contents are not exported through the MSAA interface. The ``IAccessible`` object for such a document informs the client that the document is protected.

.. _section-19:

 
 

+-------------------+--------------------------------------------------------------------------------------------------------------+
| Method            | Implementation notes                                                                                         |
+===================+==============================================================================================================+
| accHitTest        | Returns ``NULL`` .                                                                                           |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| accLocation       | The screen coordinates of the visible part of the document.                                                  |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| accNavigate       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ). |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| accSelect         | Returns ``NULL`` .                                                                                           |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accChildCount | The child count is 0.                                                                                        |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accFocus      | Returns ``NULL`` .                                                                                           |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accName       | The name is "Alert: Protection Failure".                                                                  |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accParent     | The parent is ``NULL`` .                                                                                     |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accRole       | The role is ``ROLE_SYSTEM_TEXT`` .                                                                           |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accSelection  | Returns ``NULL`` .                                                                                           |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accState      | The state is ``STATE_SYSTEM_ALERT_MEDIUM + STATE_SYSTEM_UNAVAILABLE + STATE_SYSTEM_READONLY`` .              |
+-------------------+--------------------------------------------------------------------------------------------------------------+
| get_accValue      | The value is "This document's security settings prevent access."                                          |
+-------------------+--------------------------------------------------------------------------------------------------------------+

Empty PDF Document
------------------

Represents an empty or apparently empty document. A PDF file may have no contents to export through MSAA if, for instance, the file is a scanned image that has not been run through an optical character recognition (OCR) tool. The ``IAccessible`` object for empty documents and pages informs the client that there may be a problem, even if the document or page is genuinely empty.

.. _section-20:

 
 

+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| Method            | Implementation notes                                                                                                              |
+===================+===================================================================================================================================+
| accHitTest        | Returns ``NULL`` .                                                                                                                |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| accLocation       | Returns the screen coordinates of the visible part of the document.                                                               |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| accNavigate       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                      |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| accSelect         | Returns ``NULL`` .                                                                                                                |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount | The child count is 0.                                                                                                             |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus      | Returns ``NULL`` .                                                                                                                |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accName       | The name is "Alert: Empty document".                                                                                           |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accParent     | The parent is ``NULL`` .                                                                                                          |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accRole       | The role is ``ROLE_SYSTEM_TEXT`` .                                                                                                |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection  | Returns ``NULL`` .                                                                                                                |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accState      | The state is ``STATE_SYSTEM_READONLY`` .                                                                                          |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+
| get_accValue      | The value is "This document appears to be empty. It may be a scanned image that needs OCR or it may have malformed structure." |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------+

PDF Structure Element
---------------------

Represents a subtree of the logical structure tree for the document. It might correspond to a paragraph, a heading, a chapter, a span of text within a word, or a figure.

.. _section-21:

 
 

+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                                                                                                                     |
+===================================+==========================================================================================================================================================================================================================================+
| accDoDefaultAction                | If the element has state ``STATE_SYSTEM_LINKED`` , performs the action associated with the link.                                                                                                                                         |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object or any child at the given location if the location is within the bounding box of this object.                                                                                                                        |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the subtree.                                                                                                                                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Only spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ) is supported for table elements (``ROLE_SYSTEM_CELL`` , ``ROLE_SYSTEM_ROW`` , ``ROLE_SYSTEM_ROWHEADER`` , ``ROW_SYSTEM_COLUMNHEADER`` ). |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | For ``SELFLAG_TAKEFOCUS`` , sets focus to the document window and positions the document to the beginning of the structure element content. The other ``SELFLAG`` values are not supported.                                              |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChild                      | Returns a child object.                                                                                                                                                                                                                  |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | Returns the number of child objects beneath this one.                                                                                                                                                                                    |
|                                   |                                                                                                                                                                                                                                          |
|                                   | If the node has an ``Alt`` or ``ActualText`` attribute, the child count is always zero.                                                                                                                                                  |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | If the element has state ``STATE_SYSTEM_LINKED`` , returns a text description of the action associated with the link (such as "go to page 5" or "play movie").                                                                     |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                                                                                                                                                        |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | The parent is either another structure element or the document structure root.                                                                                                                                                           |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is one of:                                                                                                                                                                                                                      |
|                                   |                                                                                                                                                                                                                                          |
|                                   | ROLE_SYSTEM_GROUPING ROLE_SYSTEM_TABLE ROLE_SYSTEM_CELL ROLE_SYSTEM_ROW                                                                                                                                                                  |
|                                   | | ROLE_SYSTEM_ROWHEADER                                                                                                                                                                                                                  |
|                                   | | ROW_SYSTEM_COLUMNHEADER                                                                                                                                                                                                                |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection                  | Returns ``NULL`` .                                                                                                                                                                                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state is a logical OR of one or more of the following:                                                                                                                                                                               |
|                                   |                                                                                                                                                                                                                                          |
|                                   | | STATE_SYSTEM_READONLY                                                                                                                                                                                                                  |
|                                   | | STATE_SYSTEM_LINKED                                                                                                                                                                                                                    |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                                                                                                                                 |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                                                                                                                                                   |
|                                   |                                                                                                                                                                                                                                          |
|                                   | -  ``STATE_SYSTEM_READONLY`` is always set.                                                                                                                                                                                              |
|                                   | -  If the element is part of a link (that is, if it has an ancestor of role ``ROLE_SYSTEM_LINK`` ) then both ``STATE_SYSTEM_LINKED`` and ``STATE_SYSTEM_FOCUSABLE`` are set, and ``STATE_SYSTEM_FOCUSED`` can also be set.               |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | If this node has an ``Alt`` or ``ActualText`` attribute, the value is the contents of the attribute.                                                                                                                                     |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Content Element
-------------------

Corresponds to a leaf node of the logical structure tree for the document. It corresponds to marking commands in the page content stream.

.. _section-22:

 
 

+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                                                                                                       |
+===================================+============================================================================================================================================================================================================================+
| accDoDefaultAction                | If the element has state ``STATE_SYSTEM_LINKED`` , performs the action associated with the link.                                                                                                                           |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                                                                                                                                       |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the element.                                                                                                                                                         |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                                                                                                               |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | For ``SELFLAG_TAKEFOCUS`` , sets focus to the document window and positions the document to the beginning of the content. The other ``SELFLAG`` values are not supported.                                                  |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                                                                                                                                      |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | If the element has state ``STATE_SYSTEM_LINKED`` , describes the action associated with the link.                                                                                                                          |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                                                                                                                                          |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | The parent is either a structure element or the document structure root.                                                                                                                                                   |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is one of:                                                                                                                                                                                                        |
|                                   |                                                                                                                                                                                                                            |
|                                   | | ROLE_SYSTEM_TEXT                                                                                                                                                                                                         |
|                                   | | ROLE_SYSTEM_GRAPHIC                                                                                                                                                                                                      |
|                                   | | ROLE_SYSTEM_CLIENT                                                                                                                                                                                                       |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection                  | Returns ``NULL`` .                                                                                                                                                                                                         |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state is a logical OR of one or more of the following:                                                                                                                                                                 |
|                                   |                                                                                                                                                                                                                            |
|                                   | | STATE_SYSTEM_READONLY                                                                                                                                                                                                    |
|                                   | | STATE_SYSTEM_LINKED                                                                                                                                                                                                      |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                                                                                                                   |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                                                                                                                                     |
|                                   |                                                                                                                                                                                                                            |
|                                   | -  ``STATE_SYSTEM_READONLY`` is always set.                                                                                                                                                                                |
|                                   | -  If the element is part of a link (that is, if it has an ancestor of role ``ROLE_SYSTEM_LINK`` ) then both ``STATE_SYSTEM_LINKED`` and ``STATE_SYSTEM_FOCUSABLE`` are set, and ``STATE_SYSTEM_FOCUSED`` can also be set. |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | If this node has an ``Alt`` or ``ActualText`` attribute, the value is the content of that attribute. Otherwise, the value is all of the text contained in the marking commands for this node.                              |
+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Comment
-----------

Corresponds to a comment, such as a text note or highlight comment, attached to the document.

.. note::

   PDF comments cover a range of objects, many of which do not map into the standard MSAA roles. The ``IAccessible`` object captures the most important properties of comments.

.. _section-23:

 
 

+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                              |
+===================================+===================================================================================================================================================+
| accDoDefaultAction                | The default action depends on the type of comment. It can, for example, open or close a popup.                                                    |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                                                              |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                                                                 |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                                      |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the comment gives it the keyboard focus).                                                      |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                                                             |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | Describes the default action, which depends on the type of comment.                                                                               |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDescription                | For file attachment and sound comments, a description of the icon for the comment.                                                                |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                                                                 |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accName                       | -  The name indicates the type of comment; for example, Text Comment or Underline Comment.                                                        |
|                                   | -  If the comment is open and has a title, the name also contains the title of the comment.                                                       |
|                                   | -  If the comment is a Free Text comment or modifies a span of text (such as an Underline or Strikeout Comment), the name also contains the text. |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | The parent is either a structure element or the document structure root.                                                                          |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is one of:                                                                                                                               |
|                                   |                                                                                                                                                   |
|                                   | | ROLE_SYSTEM_TEXT                                                                                                                                |
|                                   | | ROLE_SYSTEM_WHITESPACE                                                                                                                          |
|                                   | | ROLE_SYSTEM_PUSHBUTTON                                                                                                                          |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection                  | Returns ``NULL`` .                                                                                                                                |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state is a logical OR of one or more of the following:                                                                                        |
|                                   |                                                                                                                                                   |
|                                   | | STATE_SYSTEM_READONLY                                                                                                                           |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                                                          |
|                                   | | STATE_SYSTEM_LINKED                                                                                                                             |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                                          |
|                                   | | STATE_SYSTEM_EXPANDED                                                                                                                           |
|                                   | | STATE_SYSTEM_COLLAPSED                                                                                                                          |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                                                            |
|                                   |                                                                                                                                                   |
|                                   | -  If a comment can be opened, ``STATE_SYSTEM_LINKED`` is set.                                                                                    |
|                                   | -  ``STATE_SYSTEM_EXPANDED`` and ``STATE_SYSTEM_COLLAPSED`` indicate whether the comment is open.                                                 |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | -  If the comment is open, the value is the contents of the comment pop-up window.                                                                |
|                                   | -  If the comment is a type that does not open, the value is the contents of the comment itself.                                                  |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Link
--------

Corresponds to a link in the document.

.. _section-24:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                                                                                   |
+===================================+========================================================================================================================================================================================================+
| accDoDefaultAction                | Performs the link's action.                                                                                                                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object or any child at the given location if the location is within the bounding box of this object.                                                                                      |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                                                                                                                      |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                                                                                           |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS``                                                                                                                                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChild                      | Returns a child object.                                                                                                                                                                                |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | Returns the number of children. If the node has an ``Alt`` or ``ActualText`` attribute, the child count is always zero.                                                                                |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | Describes the action defined for this link.                                                                                                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                                                                                                                      |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accName                       | If there is an ``Alt`` or ``ActualText`` attribute associated with this link, the name is the associated ``Alt`` text or ``ActualText`` . Otherwise, the name is the value of the first content child. |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | The parent is either a structure element or the document structure root.                                                                                                                               |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is ``ROLE_SYSTEM_LINK`` .                                                                                                                                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection                  | Returns ``NULL`` .                                                                                                                                                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state is a logical OR of the following:                                                                                                                                                            |
|                                   |                                                                                                                                                                                                        |
|                                   | | STATE_SYSTEM_READONLY                                                                                                                                                                                |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                                                                                                               |
|                                   | | STATE_SYSTEM_LINKED                                                                                                                                                                                  |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                                                                                               |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                                                                                                                 |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | The value is a unique identifier for each link.                                                                                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Text Form Field
-------------------

Corresponds to a text form field in the document.

.. _section-25:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                         |
+===================================+==============================================================================================================+
| accDoDefaultAction                | Sets focus to the text field for editing.                                                                    |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ). |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the field gives it the keyboard focus).                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | The default action is "DoubleClick", which sets the keyboard focus to this field.                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accName                       | The user name (short description) of the form field.                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accParent                     | Returns the parent object.                                                                                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is ``ROLE_SYSTEM_TEXT`` .                                                                           |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state of the text field is a logical OR of one of more of:                                               |
|                                   |                                                                                                              |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                     |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                   |
|                                   | | STATE_SYSTEM_READONLY                                                                                      |
|                                   | | STATE_SYSTEM_SELECTABLE                                                                                    |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                     |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                       |
|                                   | | STATE_SYSTEM_PROTECTED                                                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accValue                      | The value is the text in the text field.                                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+

PDF Button Form Field
---------------------

Corresponds to a button form field in the document.

.. _section-26:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                         |
+===================================+==============================================================================================================+
| accDoDefaultAction                | Presses the button.                                                                                          |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ). |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the field gives it the keyboard focus).                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | The default action is "Press".                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accName                       | The user name of the form field (short description).                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accParent                     | Returns the parent object.                                                                                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is ``ROLE_SYSTEM_PUSHBUTTON`` .                                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state of the button is a logical OR of one or more of:                                                   |
|                                   |                                                                                                              |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                     |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                   |
|                                   | | STATE_SYSTEM_READONLY                                                                                      |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                     |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                       |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+

PDF CheckBox Form Field
-----------------------

Corresponds to a checkbox form field in the document.

.. _section-27:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                         |
+===================================+==============================================================================================================+
| accDoDefaultAction                | Checks or unchecks the box.                                                                                  |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ). |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the field gives it the keyboard focus).                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | -  If the check box has been selected, the default action is "UnCheck".                                   |
|                                   | -  If the check box has not been selected, the default action is "Check".                                 |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accName                       | The user name (short description) of the form field.                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accParent                     | Returns the parent object.                                                                                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is ``ROLE_SYSTEM_CHECKBUTTON`` .                                                                    |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state of the check box is a logical OR of one or more of:                                                |
|                                   |                                                                                                              |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                     |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                   |
|                                   | | STATE_SYSTEM_READONLY                                                                                      |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                     |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                       |
|                                   | | STATE_SYSTEM_CHECKED                                                                                       |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+

PDF RadioButton Form Field
--------------------------

Corresponds to a radio button form field in the document.

.. _section-28:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                         |
+===================================+==============================================================================================================+
| accDoDefaultAction                | Clicks the radio button.                                                                                     |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ). |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the field gives it the keyboard focus).                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | The default action is "Check".                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accName                       | The user name (short description) of the form field.                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accParent                     | Returns the parent object.                                                                                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is ``ROLE_SYSTEM_RADIOBUTTON`` .                                                                    |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state of the radio button is a logical OR of one or more of:                                             |
|                                   |                                                                                                              |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                     |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                   |
|                                   | | STATE_SYSTEM_READONLY                                                                                      |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                     |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                       |
|                                   | | STATE_SYSTEM_CHECKED                                                                                       |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------+

PDF ComboBox Form Field
-----------------------

Corresponds to a combo box form field in the document. It can represent either the combo box itself, or a list item in a combo box.

.. _section-29:

 
 

+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                  |
+===================================+=======================================================================================================================================+
| accDoDefaultAction                | -  The combo box does not have a default action.                                                                                      |
|                                   | -  For a list item, the default action is "DoubleClick", which selects the list item.                                              |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | -  For a combo box, returns this object or any child at the given location if the location is within the bounding box of this object. |
|                                   | -  For a list item, returns this object if the given location is within the bounding box of this object.                              |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | -  For a combo box, returns the screen coordinates of the visible part of the object.                                                 |
|                                   | -  For a list item, the location is always reported as 0,0,0,0.                                                                       |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | -  Spatial directions ``NAVDIR_UP`` and ``NAVDIR_DOWN`` are available for list items.                                                 |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | -  The combo box supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the field gives it the keyboard focus).                           |
|                                   | -  For a list item, sets the combo box to the list item value.                                                                        |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accChild                      | -  For a combo box, gets the child items.                                                                                             |
|                                   | -  A list item has no children.                                                                                                       |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | -  For a combo box, the child count is the number of items in the list.                                                               |
|                                   | -  For a list item, the child count is 0.                                                                                             |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | -  The combobox does not have a default action.                                                                                       |
|                                   | -  For a list item, the default action is "DoubleClick", which selects the list item.                                              |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | -  Returns the object that has the keyboard focus if it is this object or its child.                                                  |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accName                       | -  For a combo box, the name is the user name (short description) of the form field if it has been defined.                           |
|                                   | -  For a list item, the name is the text of the list item.                                                                            |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | -  Returns the parent object.                                                                                                         |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection                  | -  Returns ``NULL`` .                                                                                                                 |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | -  For a combo box, the role is ``ROLE_SYSTEM_COMBOBOX`` .                                                                            |
|                                   | -  For a list item, the role is ``ROLE_SYSTEM_LISTITEM`` .                                                                            |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | -  For a combo box, the state is a logical OR of one or more these values:                                                            |
|                                   |                                                                                                                                       |
|                                   | | STATE_SYSTEM_INVISIBLEc                                                                                                             |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                                            |
|                                   | | STATE_SYSTEM_READONLY                                                                                                               |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                              |
|                                   |                                                                                                                                       |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                                                |
|                                   | | STATE_SYSTEM_SELECTABLE                                                                                                             |
|                                   | | STATE_SYSTEM_SELECTED                                                                                                               |
|                                   |                                                                                                                                       |
|                                   | -  For a list box item, the state is a logical OR of one or more these values:                                                        |
|                                   |                                                                                                                                       |
|                                   | | STATE_SYSTEM_READONLY                                                                                                               |
|                                   | | STATE_SYSTEM_SELECTABLE                                                                                                             |
|                                   | | STATE_SYSTEM_SELECTED                                                                                                               |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                                              |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                                            |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | -  For a combo box, the value is the text value of the currently selected list item.                                                  |
|                                   | -  For a list item, the value is the text of the list item.                                                                           |
+-----------------------------------+---------------------------------------------------------------------------------------------------------------------------------------+

PDF List Box Form Field
-----------------------

Corresponds to a list box form field in the document. It can represent either the list box itself or a list item in a list box.

.. _section-30:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                 |
+===================================+======================================================================================================================================+
| accDoDefaultAction                | -  The list box does not have a default action.                                                                                      |
|                                   | -  For a list item, the default action is "Double Click," which selects the item.                                                 |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | -  For a list box, returns this object or any child at the given location if the location is within the bounding box of this object. |
|                                   | -  For a list item, returns this object if the given location is within the bounding box of this object.                             |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | -  For a list box, returns the screen coordinates of the visible part of the object.                                                 |
|                                   | -  For a list item, the location is always reported as 0,0,0,0.                                                                      |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | -  Spatial directions ``NAVDIR_UP`` and ``NAVDIR_DOWN`` are available for list items.                                                |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | -  The list box supports ``SELFLAG_TAKEFOCUS`` (that is, selecting the field gives it the keyboard focus).                           |
|                                   | -  For a list item, sets the list box selection to the list item value.                                                              |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accChild                      | -  For a list box, gets the child items.                                                                                             |
|                                   | -  A list item has no children.                                                                                                      |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | -  For a list box, the child count is the number of items in the list box.                                                           |
|                                   | -  For a list item, the child count is 0.                                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | -  The list box does not have a default action.                                                                                      |
|                                   | -  For a list item, the default action is "Double Click," which selects the item.                                                 |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | -  Returns the object that has the keyboard focus if it is this object or its child.                                                 |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accName                       | -  For a list box, the name is the user name (short description) for the form field.                                                 |
|                                   | -  For a list item, the name is the text of the list item.                                                                           |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | -  Returns the parent object.                                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | -  For a list box, the role is ``ROLE_SYSTEM_LIST`` .                                                                                |
|                                   | -  For a list item, the role is ``ROLE_SYSTEM_LISTITEM`` .                                                                           |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | -  For a list box, the state is a logical OR of one or more these values:                                                            |
|                                   |                                                                                                                                      |
|                                   | | STATE_SYSTEM_INVISIBLEc                                                                                                            |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                                           |
|                                   | | STATE_SYSTEM_READONLY                                                                                                              |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                             |
|                                   |                                                                                                                                      |
|                                   | -  For a list item, the state is a logical OR of one or more these values:                                                           |
|                                   |                                                                                                                                      |
|                                   | | STATE_SYSTEM_READONLY                                                                                                              |
|                                   | | STATE_SYSTEM_SELECTABLE                                                                                                            |
|                                   | | STATE_SYSTEM_SELECTED                                                                                                              |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                                             |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                                           |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accSelection                  | -  Returns ``NULL`` .                                                                                                                |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | -  For a list box, the value is the text value of the currently selected list item.                                                  |
|                                   | -  For a list item, the ``Value`` attribute is the text of the list item.                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------+

PDF Digital Signature Form Field
--------------------------------

Corresponds to a digital signature form field in the document.

.. _section-31:

 
 

+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                                                                                                                                         |
+===================================+==============================================================================================================================================================================================================================================================+
| accDoDefaultAction                | Signs the document if the signature field is unsigned and has either been opened with Acrobat or the document has permissions that allow signing. If the document is signed, the default action brings up a dialog box containing the signature information. |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                                                                                                                                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the visible part of the object.                                                                                                                                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accNavigate                       | Does not support spatial navigation (``NAVDIR_UP`` , ``NAVDIR_DOWN`` , ``NAVDIR_RIGHT`` , ``NAVDIR_LEFT`` ).                                                                                                                                                 |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accSelect                         | Supports ``SELFLAG_TAKEFOCUS`` .                                                                                                                                                                                                                             |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                                                                                                                                                                        |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDefaultAction              | Returns ``NULL`` .                                                                                                                                                                                                                                           |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accFocus                      | Returns the object that has the keyboard focus if it is this object or its child.                                                                                                                                                                            |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accName                       | The user name (short description) of the form field.                                                                                                                                                                                                         |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | Returns the parent object.                                                                                                                                                                                                                                   |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The Digital Signature form field does not map to any of the existing roles, and a custom role, ``Signature`` , has been defined for it.                                                                                                                      |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | The ``State`` attribute of the digital signature is a logical OR of one of more of these values:                                                                                                                                                             |
|                                   |                                                                                                                                                                                                                                                              |
|                                   | | STATE_SYSTEM_INVISIBLE                                                                                                                                                                                                                                     |
|                                   | | STATE_SYSTEM_UNAVAILABLE                                                                                                                                                                                                                                   |
|                                   | | STATE_SYSTEM_READONLY                                                                                                                                                                                                                                      |
|                                   | | STATE_SYSTEM_FOCUSABLE                                                                                                                                                                                                                                     |
|                                   | | STATE_SYSTEM_FOCUSED                                                                                                                                                                                                                                       |
|                                   | | STATE_SYSTEM_CHECKED                                                                                                                                                                                                                                       |
|                                   | | STATE_SYSTEM_TRAVERSED                                                                                                                                                                                                                                     |
|                                   |                                                                                                                                                                                                                                                              |
|                                   | -  If ``STATE_SYSTEM_CHECKED`` is set, but not ``STATE_SYSTEM_TRAVERSED`` , the signature is unverified.                                                                                                                                                     |
|                                   | -  If ``STATE_SYSTEM_TRAVERSED`` is set, but not ``STATE_SYSTEM_CHECKED`` , the signature is invalid.                                                                                                                                                        |
|                                   | -  If both ``STATE_SYSTEM_CHECKED`` and ``STATE_SYSTEM_TRAVERSED`` are set, the signature is valid.                                                                                                                                                          |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | The ``Value`` attribute is the name and date of the signature, if that information is present.                                                                                                                                                               |
+-----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

PDF Caret
---------

Represents a caret (text cursor). If a document contains the system caret because focus is within an editable text field or an editable ComboBox field, clients can obtain an ``IAccessible`` object for the caret to determine where it is located.

.. _section-32:

 
 

+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Method                            | Implementation notes                                                                                                                                             |
+===================================+==================================================================================================================================================================+
| accHitTest                        | Returns this object if the given location is within the bounding box of this object.                                                                             |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| accLocation                       | Returns the screen coordinates of the caret, both when the caret is in a form field and when it is in the document.                                              |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accChildCount                 | The child count is 0.                                                                                                                                            |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accDescription                | The description is a string containing the index of the character in the field that follows the caret.                                                           |
|                                   |                                                                                                                                                                  |
|                                   | If the caret is at the beginning of the field, the description string is "0". If the caret follows the first character, the description string is "1".     |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accParent                     | The parent is the field containing the caret. However, the caret ``IAccessible`` object is not listed among the children of that field's ``IAccessible`` object. |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accRole                       | The role is ``ROLE_SYSTEM_CARET`` .                                                                                                                              |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accState                      | The state is 0.                                                                                                                                                  |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| get_accValue                      | The value is the current value of the Text field or ComboBox form field containing the caret.                                                                    |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
