'''Defines all input and output classes for translation Apps related API endpoints'''

from typing import List, Tuple
from enum import Enum
from pydantic import BaseModel, Field, constr, root_validator
from schemas import LangCodePattern, BookCodePattern, TableNamePattern
from schemas import LanguageResponse


class TranslationDocumentType(Enum):
    '''Currently supports bible USFM only. Can be extended to
    CSV(for commentary or notes), doc(stories, other passages) etc.'''
    USFM = 'usfm'
    TEXT = 'text'
    CSV = 'csv'
    JSON = 'alignment-json'

class Stopwords(BaseModel):
    '''Input object for stopwords'''
    prepositions: List[str] = Field(...,
        example=["कोई", "यह", "इस","इसे", "उस", "कई","इसी", "अभी", "जैसे"])
    postpositions: List[str] = Field(...,
        example=["के", "का", "में", "की", "है", "और", "से", "हैं", "को", "पर"])

class TranslationProjectCreate(BaseModel):
    '''Input object for project creation'''
    projectName: str = Field(..., example="Hindi Malayalam Gospels")
    sourceLanguageCode : LangCodePattern =Field(...,example='hin')
    targetLanguageCode : LangCodePattern =Field(...,example='mal')
    documentFormat: TranslationDocumentType = TranslationDocumentType.USFM
    useDataForLearning: bool = True
    stopwords: Stopwords = None
    punctuations: List[constr(max_length=1)] = Field(None,
        example=[',', '"', '!', '.', ':', ';', '\n', '\\','“','”',
        '“','*','।','?',';',"'","’","(",")","‘","—"])
    active: bool = True

class TranslationProject(BaseModel):
    '''Output object for project creation'''
    projectId: int= Field(..., example=100001)
    projectName: str= Field(..., example="Hindi Malayalam Gospels")
    sourceLanguage : LanguageResponse = Field(...)
    targetLanguage : LanguageResponse = Field(...)
    documentFormat: TranslationDocumentType
    metaData: dict = Field(None, example={"books":['mat', 'mrk', 'luk', 'jhn'],
        "use_data_for_learning":True})
    active: bool
    class Config: # pylint: disable=too-few-public-methods
        ''' telling Pydantic exactly that "it's OK if I pass a non-dict value,
        just get the data from object attributes'''
        orm_mode = True

class SelectedBooks(BaseModel):
    '''List of selected books from an existing bible in the server'''
    bible: TableNamePattern = Field(..., example='hin_IRV_1_bible')
    books: List[BookCodePattern]= Field(..., example=['luk', 'jhn'])

class TranslationProjectEdit(BaseModel):
    '''New books to be added or active flag change'''
    projectId: int
    active: bool = None
    selectedBooks: SelectedBooks = None
    uploadedBooks: List[str] = None
    useDataForLearning: bool = None
    stopwords: Stopwords = None
    punctuations: List[constr(max_length=1)] = None

class TranslationProjectUpdateResponse(BaseModel):
    '''Response for post and put'''
    message:str = Field(...,example="Project created/updated successfully")
    data: TranslationProject = None

class TokenOccurence(BaseModel):
    '''Object for token occurence'''
    sentenceId: int = Field(..., example=41001001)
    offset: List[int] = Field(..., min_items=2, max_items=2, example=(0,8))

class Token(BaseModel):
    '''Response object for token'''
    token: str = Field(..., example='इब्राहीम')
    occurrences: List[TokenOccurence]
    translations: dict = Field(...,
        example={'അബ്രാഹാമിന്റെ':{"frequency":10}, 'അബ്രാഹാം':{"frequency":24}})
    metaData: dict = Field(None, example={"translationWord": "Abraham",
    	"link": "https://git.door43.org/unfoldingWord/en_tw/src/branch/master/bible/names/abraham.md"})
    class Config: # pylint: disable=too-few-public-methods
        ''' telling Pydantic exactly that "it's OK if I pass a non-dict value,
        just get the data from object attributes'''
        orm_mode = True

class TokenUpdate(BaseModel):
    '''Input object for applying token translation'''
    token: str = Field(..., example="इब्राहीम")
    occurrences: List[TokenOccurence]
    translation: str = Field(..., example="അബ്രാഹാം")

class Sentence(BaseModel):
    '''Response object for sentences and plain-text draft'''
    sentenceId: int
    sentence: str
    draft: str = None
    draftMeta: List[Tuple[Tuple[int, int], Tuple[int,int],'str']] = Field(None,
        example=[[[0,8], [0,8],"confirmed"],
            [[8,64],[8,64],"untranslated"]])
    class Config: # pylint: disable=too-few-public-methods
        ''' telling Pydantic exactly that "it's OK if I pass a non-dict value,
        just get the data from object attributes'''
        orm_mode = True

class TranlsateResponse(BaseModel):
    '''response object after applying token translations'''
    message: str = Field(..., example="Token translations saved")
    data:List[Sentence] = None

class DraftInput(BaseModel):
    '''Input sentences for translation'''
    sentenceId: str = Field(..., example=41001001)
    sentence: str = Field(...,
    	example="इब्राहीम के वंशज दाऊद के पुत्र यीशु मसीह की वंशावली इस प्रकार है")
    draft: str = None
    draftMeta: List[Tuple[Tuple[int, int], Tuple[int,int],'str']] = Field(None,
        example=[[[0,8], [0,8],"confirmed"],
            [[8,64],[8,64],"untranslated"]])
    @root_validator
    def set_surrogate_id(cls, values): # pylint: disable=R0201 disable=E0213
        '''USFM and JSON should be updated together. If they are absent, bookCode is required'''
        values['surrogateId'] = values['sentenceId']
        try:
            values['sentenceId'] = int(values['sentenceId'])
        except Exception as e:
            raise e
        return values

class SentenceInput(BaseModel):
    '''Input sentences for tokenization'''
    sentenceId: str = Field(..., example=41001001)
    sentence: str = Field(...,
        example="इब्राहीम के वंशज दाऊद के पुत्र यीशु मसीह की वंशावली इस प्रकार है")
    @root_validator
    def set_surrogate_id(cls, values): # pylint: disable=R0201 disable=E0213
        '''USFM and JSON should be updated together. If they are absent, bookCode is required'''
        values['surrogateId'] = values['sentenceId']
        try:
            values['sentenceId'] = int(values['sentenceId'])
        except Exception as e:
            raise e
        return values


class DraftFormats(Enum):
    '''Specify various export,view,download formats for project/draft'''
    USFM = 'usfm'
    JSON = 'alignment-json'

class Suggestion(BaseModel):
    '''Response object for suggestion'''
    suggestion:str
    score: float

class Progress(BaseModel):
    '''Response object for AgMT project progress'''
    confirmed: float
    suggestion: float
    untranslated: float
