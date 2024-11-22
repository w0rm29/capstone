import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, Checkbox, ListItemText } from '@mui/material';

interface MultiSelectDropdownProps {
  tag: string[];
  setTag: React.Dispatch<React.SetStateAction<string[]>>;
  options: string[];
}

const MultiSelectDropdown: React.FC<MultiSelectDropdownProps> = ({ tag, setTag, options }) => {
  return (
    <FormControl variant="outlined" fullWidth>
      <InputLabel>Tag</InputLabel>
      <Select
        label="Tag"
        multiple
        value={tag}
        onChange={(e) => setTag(e.target.value as string[])}
        renderValue={(selected) => (Array.isArray(selected) ? selected.join(', ') : '')}
      >
        {options.map((option) => (
          <MenuItem key={option} value={option}>
            <Checkbox checked={tag.includes(option)} />
            <ListItemText primary={option} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default MultiSelectDropdown;
