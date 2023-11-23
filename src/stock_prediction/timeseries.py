from typing import Any, Optional, Literal, Union
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from pandas._libs.tslibs.timestamps import Timestamp
from scipy.interpolate import interp1d


class TimeSeries:
    DATE_COLUMN_TYPE: str = '<M8[ns]'
    ITERPOLATION_KIND: str = "linear"
    __REFDATE__ = datetime(2000,1,1)

    def __init__(
        self,
        df: pd.DataFrame,
        min_date: Union[str, Timestamp, datetime],
        max_date: Union[str, Timestamp, datetime],
        time_column: Optional[str] = None,
        format: str = "%Y-%m-%d",
        period: Literal["daily", "weekly", "monthly", "annualy"] = "daily",  
    ):
        self.df = df
        self.min_date = min_date
        self.max_date = max_date
        self.time_column = time_column
        self.format = format
        self.period = self._interpret_period(period)
        self.__ref_date = datetime
        self._format_dataframe()
        self._convert_bound_dates()
        self.interpolators = {}

    def _format_dataframe(self):
        if self.time_column:
            self.df = self.df.set_index(self.time_column)
        self.df.index = pd.to_datetime(self.df.index)
        self._verify_if_index_is_a_date()

    def _verify_if_index_is_a_date(self):
        if self.df.index.dtype != self.DATE_COLUMN_TYPE:
            message = f"Time column must be in the format {self.DATE_COLUMN_TYPE}"
            raise TypeError(message)

    def _convert_bound_dates(self):
        self.min_date = pd.to_datetime(self.min_date, format=self.format)
        self.max_date = pd.to_datetime(self.max_date, format=self.format)

    def _interpret_period(self, period):
        period_in_days_mapping = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
            "annualy": 364,
        }
        return period_in_days_mapping.get(period, None)


    def interpolate(self):
        result = pd.DataFrame()
        for col in self.df:
            interp_column = self._interp_column(self.df[col], self.df.index)
            result = result.merge(interp_column, how="outer", left_index=True, right_index=True)
        return result


    def _interp_column(self, column, dates):

        delta_days = (dates - self.__REFDATE__).days
        min_delta_days = delta_days.min()
        max_delta_days = delta_days.max()

        array = np.array([[x,y] for x, y in zip(delta_days.values,column.values) if not pd.isnull(y)])
        self.interpolators[column.name] = interp1d(array[:,0], array[:,1], kind=self.ITERPOLATION_KIND, bounds_error=False)

        
        min_days = (self.min_date-self.__REFDATE__).days
        max_days = (self.max_date-self.__REFDATE__).days

        days = np.arange(min_days, max_days, self.period)
        if ((max_days - min_days) % self.period) > 0:
            days = np.array(list(days) + [max_days])
        interpolations = self.interpolators[column.name](days)

        values = np.array([[self.__REFDATE__ + timedelta(int(x)),y] for x, y in zip(days, interpolations) if ( min_delta_days <= x <= max_delta_days)])

        return pd.DataFrame(values, columns=["date", column.name]).set_index("date")

