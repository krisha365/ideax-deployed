Create a folder named "media" before starting the project
 1. install wysiwyg library by:
  pip install django-wysiwyg
 2. install ckeditor:
  pip install django-ckeditor
 3. run "python manage.py makemigrations"
 4. run "python manage.py migrate"


Database updated
blog's data will be inserted into database after clicking onto "Save as draft" button in preview.html

"Post" functionality implemented.

Custom CKeditor
In config.js file of ckeditor add:
 CKEDITOR.editorConfig = function( config ) {
	
  config.height = 300
  config.width = 800

  config.toolbar = [
   { name: 'clipboard', items: [ 'Cut', 'Copy', '-', 'Undo', 'Redo' ] },
   { name: 'editing', items: [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ] },
   '/',
   { name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'CopyFormatting', 'RemoveFormat' ] },
   { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-' ] },
   { name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] },
   { name: 'insert', items: [ 'HorizontalRule', 'SpecialChar' ] },
   { name: 'tools', items: [ 'Maximize' ] }
  ];
};
