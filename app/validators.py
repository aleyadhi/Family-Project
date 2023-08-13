from django.core.exceptions import ValidationError



education_list = ['Doctorate degree', 
                  'Master degree', 
                  'Bachelor degree',
                  'HighSchool',
                  'Middle School',
                  'Primary School',
                 ]


def EducationStages(value):
    if value not in education_list:
        raise ValidationError(f'{value} is not valid unit of measure')