import * as React from 'react';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import dayjs, { Dayjs } from 'dayjs';

interface DatePickerProps {
  date: Dayjs | null
  onChange: (value: Dayjs | null) => void; 
}

const BasicDateCalendar: React.FC<DatePickerProps> = ({ date, onChange }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DemoContainer components={['DateTimePicker']}>
        <DateTimePicker 
        label="Basic date time picker" 
        onChange={onChange}
        value={date}
        minDate={dayjs()}
        maxDate={dayjs("9999-12-31")}
        />
      </DemoContainer>
    </LocalizationProvider>
  );
}

export default BasicDateCalendar;
