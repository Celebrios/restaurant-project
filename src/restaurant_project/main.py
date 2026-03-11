from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

app = FastAPI()