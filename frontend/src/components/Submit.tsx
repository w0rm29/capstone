import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import axios from "axios";
import { TextField } from '@mui/material';
import BasicDateCalendar from './DatePicker';
import dayjs, { Dayjs } from 'dayjs';

export default function BasicButtons() {
  const [todo, settodo] = React.useState('');
  const [startDate, setStartdate] = React.useState<Dayjs | null>(null);
  const [endDate, setEnddate] = React.useState<Dayjs | null>(null);
  const [tag, settag] = React.useState('');

  async function handleSubmit() {
    const submitData = {
      todo: todo, 
      tag: tag,
      start_date: startDate?.toISOString(),
      end_date: endDate?.toISOString()
    };

    console.log("Submit Data:", submitData);

    const { data } = await axios.post(`http://0.0.0.0:8000/todo/create`, submitData);
    console.log("submitted", submitData);
    alert(data.message);
    settodo('');
    settag('');
    setStartdate(dayjs);
    setEnddate(dayjs);
  }

  return (
    <div>
      <Stack spacing={2} direction="row">
        <TextField
          label="Todo"
          variant="outlined"
          value={todo}
          onChange={(e) => settodo(e.target.value)}
        />
        <TextField
          label="Tag"
          variant="outlined"
          value={tag}
          onChange={(e) => settag(e.target.value)}
        />
      </Stack>

      <Stack spacing={2} direction="row">
        <BasicDateCalendar date={startDate} onChange={setStartdate} />
        <BasicDateCalendar date={endDate} onChange={setEnddate} />
      </Stack>

      <Button variant="outlined" onClick={handleSubmit}>Submit</Button>
    </div>
  );
}
