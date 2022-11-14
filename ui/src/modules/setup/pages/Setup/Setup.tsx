import { Refresh as RefreshIcon } from '@mui/icons-material';
import {
  Grid,
  IconButton,
  MenuItem,
  Select,
  SelectChangeEvent,
  Stack,
  Typography,
} from '@mui/material';
import { ReactNode, useContext, useEffect, useState } from 'react';
import { Context } from '../../../../components/Context';

export const Setup = () => {
  const { context, setContext } = useContext(Context);
  const [windows, setWindows] = useState([]);
  const handleOnChangeWindow = async (
    event: SelectChangeEvent<string>,
    _: ReactNode
  ) => {
    const selectedWindow = event.target.value;
    const newContext = { ...context, window: selectedWindow };
    // @ts-ignore
    await window.api.setContext(newContext);
    setContext(newContext);
  };
  const getWindows = async () => {
    try {
      // @ts-ignore
      const availableWindows = await window.api.getWindows();
      setWindows(availableWindows);
    } catch (err) {
      console.log(`🚀 ~ error getting windows`, err);
    }
  };
  useEffect(() => {
    getWindows();
  }, []);
  return (
    <Stack direction='column'>
      <Typography>Available SO windows</Typography>
      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Select
            fullWidth
            label='Windows'
            value={context.window}
            onChange={handleOnChangeWindow}
          >
            {windows.map((window) => (
              <MenuItem key={window} value={window}>
                {window}
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={2}>
          <IconButton color='primary' component='label'>
            <RefreshIcon onClick={getWindows} />
          </IconButton>
        </Grid>
      </Grid>
    </Stack>
  );
};
