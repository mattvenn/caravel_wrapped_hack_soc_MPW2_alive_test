import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, First, with_timeout
import sys

async def test_start(dut):
    dut.RSTB <= 0
    dut.power1 <= 0;
    dut.power2 <= 0;
    dut.power3 <= 0;
    dut.power4 <= 0;

    await ClockCycles(dut.clock, 8)
    dut.power1 <= 1;
    await ClockCycles(dut.clock, 8)
    dut.power2 <= 1;
    await ClockCycles(dut.clock, 8)
    dut.power3 <= 1;
    await ClockCycles(dut.clock, 8)
    dut.power4 <= 1;

    await ClockCycles(dut.clock, 80)
    dut.RSTB <= 1


@cocotb.test()
async def test_all(dut):
    clock = Clock(dut.clock, 40, units="ns")
    cocotb.fork(clock.start())

    await test_start(dut)

    print("Project reset done")

    # hack_external_reset
    dut.mprj_io[26].value = 0


    # await ClockCycles(dut.clock, 12000)

    

    print("Waiting for the rom loader to start...")
    
    count = 0
    while(dut.uut.mprj.la_data_in[10].value.binstr!='1' and count < 8000):
        count = count + 1
        await(ClockCycles(dut.uut.clock, 1))
    
    if(count==8000):
        sys.exit("Wait for rom_loader_load timed out")


    print("Letting the program run for 4000 cycles")
    await ClockCycles(dut.clock, 4000)





    # for i in range(0,24):
    #     await ClockCycles(dut.uut.mprj.mprj.soc.hack_clk, 1)
    #     print("PC: ", int(dut.uut.mprj.mprj.soc.hack_pc.value), " INSTRUCTION:", hex(dut.uut.mprj.mprj.soc.hack_instruction.value))
    #     if(i==4):
    #         # Set first word of the screen to 0x53ED
    #         # In vram the bits are saved inverted, so 0x53ED becomes 0xB7CA
    #         assert(dut.vram.MemoryBlock[0] == 0xB7)
    #         assert(dut.vram.MemoryBlock[1] == 0xCA)
    #         print("  vram instruction write check passed")
    #     if(i==7):
    #         # Set Memory[4] = 0x53ED
    #         assert(dut.ram.MemoryBlock[4*2] == 0x53)
    #         assert(dut.ram.MemoryBlock[4*2+1] == 0xED)
    #         print("  ram instruction write check passed")
    #     if(i==11):
    #         # Read Keyboard and store value on Memory[5]
    #         # Firmware inputs keycode 0x61 thourgh LA[8:1]
    #         assert(dut.ram.MemoryBlock[5*2] == 0x00)
    #         assert(dut.ram.MemoryBlock[5*2+1] == 0x61)
    #         print("  keyboard read and memory write check passed")
    #     if(i==13):
    #         # Loop forever incrementing Memory[6]=Memory[6]+1
    #         # Memory[6] = 0
    #         assert(dut.ram.MemoryBlock[6*2] == 0x00)
    #         assert(dut.ram.MemoryBlock[6*2+1] == 0x00)
    #     if(i==15):            
    #         # Loop forever incrementing Memory[6]=Memory[6]+1
    #         # Memory[6] = 1            
    #         assert(dut.ram.MemoryBlock[6*2] == 0x00)
    #         assert(dut.ram.MemoryBlock[6*2+1] == 0x01)
    #     if(i==19):            
    #         # Loop forever incrementing Memory[6]=Memory[6]+1
    #         # Memory[6] = 2
    #         assert(dut.ram.MemoryBlock[6*2] == 0x00)
    #         assert(dut.ram.MemoryBlock[6*2+1] == 0x02)            
    #     if(i==23):            
    #         # Loop forever incrementing Memory[6]=Memory[6]+1
    #         # Memory[6] = 3
    #         assert(dut.ram.MemoryBlock[6*2] == 0x00)
    #         assert(dut.ram.MemoryBlock[6*2+1] == 0x03)
    #         print("  incremental loop check passed")
    


    # await ClockCycles(dut.uut.mprj.mprj.soc.hack_clk, 5)

    # print("All checks passed")

    
    # encoder0 = Encoder(dut.clk, dut.enc0_a, dut.enc0_b, clocks_per_phase = clocks_per_phase, noise_cycles = clocks_per_phase / 4)

