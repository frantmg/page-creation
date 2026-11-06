import { createTheme } from '@mui/material/styles';
import type { Shadows } from '@mui/material/styles';
const ink = '11 37 69'; // darkest brand neutral, as R G B
const soft = (y: number, blur: number, spread: number, a: number) => `0 ${y}px ${blur}px ${spread}px rgb(${ink} / ${a})`;
const shadows = ['none', soft(12, 32, -8, 0.08), soft(18, 48, -12, 0.1), soft(24, 64, -16, 0.12),
  ...Array(21).fill(soft(32, 80, -20, 0.14))] as Shadows; // replaces MUI's shallow default elevations
export const theme = createTheme({
  shadows,
  palette: { primary: { main: '#1463FF', contrastText: '#FFFFFF' }, text: { primary: '#0B2545' } },
  typography: { fontFamily: '"Source Serif 4", serif', button: { textTransform: 'none', fontWeight: 600 } },
  shape: { borderRadius: 4 },
  components: {
    MuiButton: { defaultProps: { disableElevation: true }, styleOverrides: { root: { minHeight: 56 } } },
    MuiAccordion: { defaultProps: { disableGutters: true, elevation: 0, square: true } },
  },
});
