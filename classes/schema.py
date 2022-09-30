# be warned, major spaghetti code ahead.

class DuplicateFieldException(Exception): pass
class ForbiddenFieldException(Exception): pass

class Schema():
    def __init__(self) -> None:
        # fields should be `title: default_value`
        self.fields = {}
        self.documents = []
        self.should_log = False
    
    def log(self, message):
        if self.should_log:
            print(message)

    def add_document(self):
        """Add's a document to the Schema"""

        # variable below is used for fields
        document_fields = {}
        
        # check if we're the first document, else take the last document's id and increment
        if len(self.documents) == 0:
            document_fields.__setitem__('id', 0)
        else:
            document_fields.__setitem__('id', self.documents[-1].__getitem__('id') + 1)
        
        # copy fields to document fields alongside default values
        for field in self.fields:
            document_fields.__setitem__(field, self.fields[field])
        
        # append to documents
        self.documents.append(document_fields)
    
    def get_field(self, title: int):
        """Get a document in the schema"""
        # return the get document
        return self.documents[title]
    
    def add_field(self, title: str, value=None) -> None:
        """Add's a field to the Schema"""

        # you shouldn't be able to add an id field
        if title.lower() == 'id':
            raise ForbiddenFieldException
        
        # just set the field already
        self.set_field(title, value)

        # update documents
        for doc in self.documents:
            doc.__setitem__(title, value)
            self.log(f'Set {title} to {value}')
        self.log('Done')

    def set_field(self, title: str, value=None) -> None:
        """Set a field in the Schema"""

        # like add_field but just sets the default value
        if title.lower() == 'id':
            raise ForbiddenFieldException
        self.fields.__setitem__(title.lower(), value)
        return self.get_field(title=title)
    
    def get_field(self, title: str):
        """Get a field in the schema"""
        # return the get field
        return self.fields.__getitem__(title.lower())
    
    def get_document_by_id(self, id: int):
        """Get a document by it's ID"""

        for document in self.documents:
            if document.id == id:
                return document
        return None
    
    def list_schema(self):
        """Output an array of strings that you use '\n'.join() with to create a discord formatted Schema."""

        # used PURELY for rendering to discord. massive spaghetti code.
        # if you do somehow decide to contribute to this piece of spaghetti,
        # good luck.

        render_output = []
        render_output.append('```')
        render_output.append(f'Schema Fields:')
        if not self.fields:
            render_output.append('No field data detected.')
        else:
            for field in self.fields:
                field_data = self.fields[field]
                render_output.append(f'{field}: {str(field_data)}')
        render_output.append('')

        render_output.append('Schema Documents:')
        if not self.documents:
            render_output.append('No documents detected.')
        else:
            for document in self.documents:
                render_output.append('-----')
                for field in document:
                    render_output.append(f'{field}: {document[field]}')
        render_output.append('```')

        return render_output