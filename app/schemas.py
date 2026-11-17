from pydantic import BaseModel, Field, ConfigDict

class StudentCreate(BaseModel):

    roll_no : int = Field(gt=0)

    name : str = Field(min_length=2,
                       max_length=100)

    division : str = Field(min_length=1,
                           max_length=10)



class UpdateDivision(BaseModel):

    division : str = Field (min_length=1,
                            max_length=10)


class StudentResponse(BaseModel):

    roll_no : int
    name : str
    division : str

    model_config = ConfigDict(from_attributes=True)