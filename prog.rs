extern crate itoa;

#[macro_use]
extern crate bitflags;

bitflags! {
    struct Flags: u32 {
        const A = 0b00000001;
        const B = 0b00000010;
        const C = 0b00000100;
        const ABC = Self::A.bits | Self::B.bits | Self::C.bits;
    }
}

fn main() {
    // write to a vector or other io::Write
    let mut buf = Vec::new();
    let result = itoa::write(&mut buf, 128u64);
    match result {
        Err(e) => {
            println!("Could not convert number: {}", e);
        }
        Ok(_f) =>  {
            println!("Converted number: {:?}", buf);
        }
    }

    let e1 = Flags::A | Flags::C;
    let e2 = Flags::B | Flags::C;
    assert_eq!((e1 | e2), Flags::ABC);   // union
    assert_eq!((e1 & e2), Flags::C);     // intersection
    assert_eq!((e1 - e2), Flags::A);     // set difference
    assert_eq!(!e2, Flags::A);           // set complement
}
