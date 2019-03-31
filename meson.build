project('cargosample', 'rust')

run_command('./get_cargo_deps.py', 'itoa', '0.3.4')
run_command('./get_cargo_deps.py', 'bitflags', '1.0.4')

itoa_sp = subproject('itoa-0.3.4')
bitflags_sp = subproject('bitflags-1.0.4')
itoa_dep = itoa_sp.get_variable('itoa_dep')
bitflags_dep = bitflags_sp.get_variable('bitflags_dep')

executable('prog', 'prog.rs',
  dependencies : [itoa_dep, bitflags_dep])
